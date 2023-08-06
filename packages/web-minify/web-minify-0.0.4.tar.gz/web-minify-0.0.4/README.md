# About web-minify

## Introduction
The all-in-one just-works-out-of-the-box does-what-you-want highly-opinionated web minifier&trade;

One day I was looking for a thoroughbred Python KISS tool that would optimize the static files of my web app. I was in a hurry and didn't want to fiddle around.

I was super happy when I found [css-html-js-minify](https://github.com/juancarlospaco/css-html-js-minify), which aaaalmost checked all my boxes.

__Aaaaalmost.....__

Turns out a few important pieces were missing;
1. Support for image formats such as .png/.jpeg
2. Support for svg
3. Support for sass
4. A command line tool that was smarter and did what I expected for directories

I tried to incorporate the tool in my workflow as it was, but I soon gave up and ended up copying the full tool source into my project and adding the features I needed out of sheer frustration. Fast worward a few months and here we are. I am polishing it into a standalone open source tool for the world to enjoy. And the rest is as they say history!


# Goals of this tool:

> NOTE: We have not reached all these goals yet, please see next section.

| Goal   |      Status |
|--------|-------------|
| All-in-one compressor/obfuscator/minifier/cruncher for most of the common static web formats | See [list of supported formats](#supported-formats). |
| Does what you hoped by default (i.e. highly opinionated) | ☑️ |
| Can be tweaked to do what you didn't want (i.e. flexible) | ☑️ |
| Small and dependency free (i.e. implemented in pure python if possible) | Only tested/used on Linux. There is hope for OSX/BSD/Posix but YMMV on Windows. |
| Available as library as well as command-line tool | ☑️ |
| Easily extensible; adding another backend can be done by writing one function | ☑️ |
| Cross platform, supports many Python 3.x versions | Only tested on Python 3.7 |

# Getting started

## Installing

```shell

# Install web-minify into your current Python environment
pip install web-minify

```


After installing, there are two ways to use this project:
 - As a command line tool
 - As a Python module

## Use as a command line tool
```shell

# Run the web-minify cli tool with help argument to see detailed usage
web-minify --help

```


The output looks like this:

<details>

```shell
$ ./web-minify.py --help
usage: web-minify.py [-h] [--version] [--format FORMAT] [--overwrite]
                     [--on-change] [--verbose] [--zipy] [--disable-js]
                     [--disable-css] [--disable-html] [--disable-svg]
                     [--disable-png] [--disable-jpeg] [--output OUTPUT]
                     [--sort] [--comments] [--timestamp] [--wrap]
                     [--set-precision NUM] [--set-c-precision NUM]
                     [--disable-simplify-colors] [--disable-style-to-xml]
                     [--disable-group-collapsing] [--create-groups]
                     [--keep-editor-data] [--keep-unreferenced-defs]
                     [--renderer-workaround] [--no-renderer-workaround]
                     [--strip-xml-prolog] [--remove-titles]
                     [--remove-descriptions] [--remove-metadata]
                     [--remove-descriptive-elements]
                     [--enable-comment-stripping] [--disable-embed-rasters]
                     [--enable-viewboxing] [--indent TYPE] [--nindent NUM]
                     [--no-line-breaks] [--strip-xml-space]
                     [--enable-id-stripping] [--shorten-ids]
                     [--shorten-ids-prefix PREFIX] [--protect-ids-noninkscape]
                     [--protect-ids-list LIST] [--protect-ids-prefix PREFIX]
                     [--error-on-flowtext]
                     input

optional arguments:
  -h, --help            show this help message and exit

general:
  General options for this program

  --version             show program's version number and exit
  --format FORMAT       Format string used to generate any output filename.
                        (Dangerous!!)
  --overwrite           Allow overwrite files in-place. Default is skip and
                        warn. NOTE: output fils are always overwritten.
                        (Dangerous!!)
  --on-change           Allow overwrite files only on source changed (detected
                        by modify time).
  --verbose             Show output during processing.
  --zipy                GZIP Processed files as '*.gz'.
  --disable-js          Copy .js files verbatim instead of processing
  --disable-css         Copy .css files verbatim instead of processing
  --disable-html        Copy .html files verbatim instead of processing
  --disable-svg         Copy .svg files verbatim instead of processing
  --disable-png         Copy .png files verbatim instead of processing
  --disable-jpeg        Copy .jpeg files verbatim instead of processing
  --output OUTPUT       Path to local output (file or folder).
  input                 Path to local input (file or folder).

common:
  Options common to many formats

  --sort                Alphabetically sort CSS Properties (CSS).
  --comments            Keep comments (CSS/HTML).
  --timestamp           Add a timestamp in output files (CSS/HTML/SVG).
  --wrap                Wrap output to ~80 chars per line (CSS).

svg optimization:
  Optimization options that are only available for SVG

  --set-precision NUM   set number of significant digits (default: 5)
  --set-c-precision NUM
                        set number of significant digits for control points
                        (default: same as '--set-precision')
  --disable-simplify-colors
                        won't convert colors to #RRGGBB format
  --disable-style-to-xml
                        won't convert styles into XML attributes
  --disable-group-collapsing
                        won't collapse <g> elements
  --create-groups       create <g> elements for runs of elements with
                        identical attributes
  --keep-editor-data    won't remove Inkscape, Sodipodi, Adobe Illustrator or
                        Sketch elements and attributes
  --keep-unreferenced-defs
                        won't remove elements within the defs container that
                        are unreferenced
  --renderer-workaround
                        work around various renderer bugs (currently only
                        librsvg) (default)
  --no-renderer-workaround
                        do not work around various renderer bugs (currently
                        only librsvg)

svg document:
  Document options that are only available for SVG

  --strip-xml-prolog    won't output the XML prolog (<?xml ?>)
  --remove-titles       remove <title> elements
  --remove-descriptions
                        remove <desc> elements
  --remove-metadata     remove <metadata> elements (which may contain license
                        or author information etc.)
  --remove-descriptive-elements
                        remove <title>, <desc> and <metadata> elements
  --enable-comment-stripping
                        remove all comments (<!-- -->)
  --disable-embed-rasters
                        won't embed rasters as base64-encoded data
  --enable-viewboxing   changes document width / height to 100pct / 100pct and
                        creates viewbox coordinates

svg output formatting:
  Output formatting options that are only available for SVG

  --indent TYPE         indentation of the output: none, space, tab (default:
                        space)
  --nindent NUM         depth of the indentation, i.e. number of spaces /
                        tabs: (default: 1)
  --no-line-breaks      do not create line breaks in output(also disables
                        indentation; might be overridden by
                        xml:space="preserve")
  --strip-xml-space     strip the xml:space="preserve" attribute from the root
                        SVG element

svg id attributes:
  ID attribute options that are only available for SVG

  --enable-id-stripping
                        remove all unreferenced IDs
  --shorten-ids         shorten all IDs to the least number of letters
                        possible
  --shorten-ids-prefix PREFIX
                        add custom prefix to shortened IDs
  --protect-ids-noninkscape
                        don't remove IDs not ending with a digit
  --protect-ids-list LIST
                        don't remove IDs given in this comma-separated list
  --protect-ids-prefix PREFIX
                        don't remove IDs starting with the given prefix

svg compatability checks:
  Compatibility check options that are only available for SVG

  --error-on-flowtext   exit with error if the input SVG uses non-standard
                        flowing text (only warn by default)

web-minify: Process all CSS/SASS/HTML/JS/SVG/PNG/JPEG found at input, either
in single file or recursively Applies common transformation to each file: +
compile (SASS -> CSS) + strip whitespace + strip comments + strip metadata +
increase compression ratio (PNG/JPEG) + sort (CSS) + timestamp + hash Provides
some options for processing: + process files in-place + process files renaming
to new form + compress results to .gz Available variables in format string
are: + {EXT} + {HASH} + {PATH} + {BASE}

```

</details>


## Use as a python module

<details>

```Python
import web_minify

settings = {
    "input": "my_originals_dir/",
    "output": "my_processed_dir/",
}

# Instanciate processor with settings we want to use
p = web_minify.processor.Processor(settings)


# Process files as per settings (this is equivalent to the commandline mode)
p. process_file()


# Process a list of files relative to input, and output them depending on settings
p. process_files_list(["input_file.svg", "input_file.html"])


# Process a single file (disregard input/output from settings
p.process_file("some_input_file.svg", "some_output_file.svg")

```

</details>

# Supported Formats

| Format   |       | Status | Tests|
|----------|-------|--------|------|
| *.html, *htm, *.tpl |  Hypertext Markup Language | Seems to work | Zero |
| *.css | Cascading Style Sheets | Seems to work | Zero |
| *.js | JavaScript | Buggy for modern syntax features | Zero |
| *.sass | Syntactically Awesome Style Sheets | Seems to work | Zero |
| *.png Portable Network Graphics | Seems to work | Zero |
| *.jpg, *.jpeg | Joint Photographic Experts Group | Seems to work | Zero |
| *.svg | Scalable Vector Graphics | Seems to work | Zero |
| *.your_file | It is made to be [extensible](#extending-web-minify) | Submit your PR! | ? |


## Extending web-minify

web-minify can be extended to support additional formats by a very simple interface:

1. Put a module under web-minify/web_minify/handlers/your_format. This can either be a moduler folder or module python source file. See css/ or html.py for example implementations.
2. Include the new function in __all__ in web-minify/web_minify/handlers/__init__.py
3. Register the new function in self.processor_map in web-minify/web_minify/processor.py

Easy as pie!

# Other Notable Features

1. Supports recursive scanning of directories
2. Supports spitting out .gz versions of files to speed up serving of static files
3. Supports some controls over each format's processing
4. Supports change detection and watch mode
5. Made to be somewhat [extensible](#extending-web-minify)

# Known Limitations and Problems:

1. Compression of modern .js haves some bugs. We welcome PRs!
2. Some of the usage pattersn of the command line tool are not implemented yet. We welcome PRs!
3. Codebase has ZERO tests. We welcome PRs!


# We welcome PRs!

If you want to contribute we welcome your code contriburtions! We are proud fo the fact that this project is a true meritocracy.


# License

Complete license is in the file [LICENSE](LICENSE) in the root of the git repo.

> GNU GPL and GNU LGPL or MIT.
> This work is free software: You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; Without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this work.
