#!/usr/bin/env python
import os
import shutil
import difflib
import web_minify.processor
from web_minify.files import generate_file_list

import logging

logger = logging.getLogger(__name__)

base_path: str = os.path.abspath(os.path.dirname(__file__))

input_path: str = os.path.abspath(os.path.join(base_path, "input/"))
output_path: str = os.path.abspath(os.path.join(base_path, "output/"))
expected_path: str = os.path.abspath(os.path.join(base_path, "expected/"))


try:
    from colorama import Fore, Back, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        __getattr__ = lambda self, name: ""

    Fore = Back = Style = ColorFallback()


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


def clear_output():
    shutil.rmtree(output_path, ignore_errors=True)


def test_regressions():
    # 1. Clear old result if any
    clear_output()
    # 2. Run tool on input
    settings = {"input": input_path, "output": output_path, "verbose": False}
    processor = web_minify.processor.Processor(settings)
    res, msg = processor.sanity_checks()
    if not res:
        logger.warning(msg)
    assert res
    processor.process_files()
    # 3. Compare output with expected
    expected_files = generate_file_list(expected_path)
    # output_files = generate_file_list(output_path)
    # logger.warning(pprint.pformat(expected_files))
    # logger.warning(pprint.pformat(output_files))
    # logger.warning(f"expected_path: {expected_path}")
    # logger.warning(f"output_path: {output_path}")
    errors = 0
    for expected_file in expected_files:
        # logger.warning(f"EXPECTED FILE: {expected_file}")
        rel = expected_file[expected_file.startswith(expected_path) and len(expected_path) + 1 :]
        # logger.warning(f"REL: {rel}")
        output_file = os.path.join(output_path, rel)
        # logger.warning(f"OUTPUTY FILE: {output_file}")
        assert os.path.exists(output_file)
        output_is_binary = output_file.endswith((".png", ".jpeg", ".jpg"))
        expected_is_binary = expected_file.endswith((".png", ".jpeg", ".jpg"))
        output_content = ""
        with open(output_file, "rb") if output_is_binary else open(output_file, "r", encoding="utf-8") as output_handle:
            output_content = output_handle.read()
        expected_content = ""
        with open(expected_file, "rb") if expected_is_binary else open(expected_file, "r", encoding="utf-8") as expected_handle:
            expected_content = expected_handle.read()
        if output_content != expected_content:
            logger.warning(f"--- Output did not matchexpected for {rel}:")
            diff = difflib.ndiff(output_content.splitlines(1), expected_content.splitlines(1))
            diff = color_diff(diff)
            logger.error("\n".join(diff))
            errors += 1
    assert errors == 0

    # 4. Clear result
    clear_output()
