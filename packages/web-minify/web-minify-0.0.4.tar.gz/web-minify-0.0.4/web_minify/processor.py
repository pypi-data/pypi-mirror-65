import os
import pprint
import datetime
from .handlers import html_minify, css_minify, js_minify, sass_minify, png_minify, jpeg_minify, svg_minify
from .files import path_is_in_path, generate_file_list, determine_file_extension
from .time import human_delta
import logging

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, settings: dict):
        self.settings = settings
        self.input = settings.get("input", None)
        self.output = settings.get("output", None)
        self.input_is_dir = self.input and os.path.isdir(self.input)
        self.input_exists = self.input and os.path.exists(self.input)
        self.output_is_dir = self.output and os.path.isdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)

        self.overwrite: bool = settings.get("overwrite", False)
        self.on_change: bool = settings.get("on_change", False)
        self.format: bool = settings.get("format", False)
        self.prefix: bool = settings.get("prefix", False)
        self.zipy: bool = settings.get("zipy", False)
        self.hash: bool = settings.get("hash", False)
        self.verbose: bool = settings.get("verbose", False)

        self.processor_map = {"sass": (sass_minify, False), "css": (css_minify, False), "html": (html_minify, False), "svg": (svg_minify, False), "js": (js_minify, False), "png": (png_minify, True), "jpeg": (jpeg_minify, True)}

        self.valid_extensions = [f".{ext}" for ext in self.processor_map.keys()]
        if self.verbose:
            logger.info("### Settings:")
            logger.info(pprint.pformat(self.settings))
            logger.info("### Valid extensions:")
            logger.info(pprint.pformat(self.valid_extensions))
        self.pool = None

    def sanity_checks(self):
        if not self.input or not self.input_exists:
            return (False, f"The input specified '{self.input}' did not exist. Input must be an existing directory or file.")
        if not self.overwrite and self.on_change:
            return (False, f"On-change will not have an effect so long as overwrite is not enabled.")
        if not self.output and not self.overwrite and not self.format:
            return (False, f"Only input '{self.input}' was specified. Without a setting for 'output', 'overwrite' and/or 'format' all processing will fail.")
        if path_is_in_path(self.input, self.output):
            return (False, f"The output '{self.output}' is a subpath of input '{self.input}'.")
        if path_is_in_path(self.output, self.input):
            return (False, f"The input '{self.input}' is a subpath of output '{self.output}'.")
        return True, None

    def process_file(self, input_path: str, output_path: str):
        if self.verbose:
            logger.info(f"Processing '{input_path}' to '{output_path}'")
        if not input_path:
            logger.warning(f"No input path specified")
            return False
        if not output_path:
            logger.warning(f"No output path specified")
            return False
        if os.path.isfile(output_path):
            if not self.overwrite:
                logger.warning(f"Trying to overwrite without overwrite enabled")
                return False
            if self.on_change:
                input_mtime = os.path.getmtime(input_path)
                output_mtime = os.path.getmtime(output_path)
                if input_mtime <= output_mtime:
                    if self.verbose:
                        logger.info(f"File not changed, skipping")
                    return True
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_dir):
                os.makedirs(name=output_dir, exist_ok=True)
            if not os.path.isdir(output_dir):
                logger.warning(f"Directory of '{output_path}' did not exist or could not be created.")
                return False
        extension = determine_file_extension(input_path)
        if not extension:
            logger.warning(f"Unknown extension '{extension}' for input file: '{input_path}'.")
            return False
        processor, is_binary = self.processor_map.get(extension, None)
        if not processor:
            logger.warning(f"Could not find processor for input file '{input_path}'.")
            return False
        original_content = None
        try:
            with open(input_path, "rb") if is_binary else open(input_path, "r", encoding="utf-8") as file:
                original_content = file.read()
        except Exception as err:
            logger.warning(f"Could not load data from input file '{input_path}': {err}.")
            return False
        if None == original_content:
            logger.warning(f"Input file '{input_path}' was empty.")
            # return False # This is only a warning and not an error
        processed_content = None
        if extension in ["js", "css", "html", "svg", "png", "jpeg"] and self.settings.get(f"disable_{extension}", False):
            # Perform copy
            # logger.info(f"SUPPOSED TO COPY: {input_path} ({extension})")
            processed_content = original_content
        else:
            # logger.info(f"SUPPOSED TO PROCESS: {input_path} ({extension})")
            processed_content = processor(original_content, self.settings)
        # logger.info(f"Content of file {input_path} was of type {type(original_content)} while processed {type(processed_content)}")
        if None == processed_content:
            logger.warning(f"Processed file for '{input_path}' was empty.")
            # return False # This is only a warning and not an error
        try:
            with open(output_path, "wb") if is_binary else open(output_path, "w", encoding="utf-8") as file:
                written = file.write(processed_content)
                if written != len(processed_content):
                    logger.warning(f"Partially written output ({written} of {len(processed_content)} bytes).")
                    return False
        except Exception as err:
            logger.warning(f"Could not write data to output file '{output_path}': {err}.")
            return False
        # All went well, go home happy!
        return True

    def process_files_list(self, list):
        start_time = datetime.datetime.now()
        success_count = 0
        # logger.info(f'Spreading workload over {multiprocessing.cpu_count()} CPU cores')
        # self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for item in list:
            input_path = item["input_path"]
            output_path = item["output_path"]
            single_start_time = datetime.datetime.now()
            success = self.process_file(input_path=input_path, output_path=output_path)
            if success:
                success_count += 1
            single_end_time = datetime.datetime.now()
            single_interval = single_end_time - single_start_time
            if single_interval > datetime.timedelta(seconds=1):
                logger.warning(f"Processing of {input_path} was slow ({human_delta(single_interval)})")
        # self.pool.close()
        # self.pool.join()
        # self.pool=None
        end_time = datetime.datetime.now()
        interval = end_time - start_time
        logger.info(f"Successful processing of {success_count}/{len(list)} items took {human_delta(interval)} total")
        return True

    def _process_existing_dir_to_existing_dir(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        # logger.info(pprint.pformat(input_paths))
        list = []
        for input_path in input_paths:
            common = os.path.commonpath((os.path.abspath(self.output), os.path.abspath(input_path)))
            rel = os.path.relpath(os.path.abspath(input_path), os.path.abspath(self.input))
            output_path = os.path.join(os.path.abspath(self.output), rel)
            list.append({"input_path": input_path, "output_path": output_path})
        # logger.info(pprint.pformat(list))
        return list

    def _process_existing_dir_to_new_dir(self):
        # This is same as _process_existing_dir_to_existing_dir but with a mkdir first
        os.mkdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        return self._process_existing_dir_to_existing_dir()

    def process_files(self):
        if self.input_is_dir:
            if self.output:
                if self.output_is_dir:
                    if self.verbose:
                        logger.info(f"existing-dir-to-existing-dir easy peasy case")
                    list = self._process_existing_dir_to_existing_dir()
                    return self.process_files_list(list)
                elif not self.output_exists:
                    if self.verbose or True:
                        logger.info(f"existing-dir-to-new-dir easy peasy case")
                    list = self._process_existing_dir_to_new_dir()
                    return self.process_files_list(list)
                else:
                    logger.error(f"existing-dir-to-existing-file error")
                    return False
                return False
            elif self.overwite:
                return False
            elif self.format:
                return False
            else:
                logger.error(f"input dir specified without valid output option")
                return False
        else:
            if self.output:
                if self.output_is_dir:
                    if self.verbose or True:
                        logger.info(f"existing-file-to-existing-dir easy peasy case NOT IMPLEMENTED YET!")
                    return False
                elif not self.output_exists:
                    if self.verbose or True:
                        logger.info(f"existing-file-to-new-file easy peasy case NOT IMPLEMENTED YET!")
                    return False
                else:
                    if self.overwite:
                        if self.verbose or True:
                            logger.info(f"existing-file-to-existing-file overwrite easy peasy case NOT IMPLEMENTED YET!")
                        return False
                    else:
                        logger.error(f"existing-file-to-existing-file non-overwrite error")
                        return False
                return False
            elif self.overwite:
                return False
            elif self.format:
                return False
            else:
                logger.error(f"input file specified without valid output option")
                return False
