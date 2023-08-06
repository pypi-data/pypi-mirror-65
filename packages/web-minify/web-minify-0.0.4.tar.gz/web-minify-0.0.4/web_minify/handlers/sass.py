from .css import css_minify

import logging

logger = logging.getLogger(__name__)

have_sass = False

try:
    import sass

    have_sass = True
except Exception:
    logger.warning("Could not import sass", exc_info=True)
    logger.warning("NOTE: To install sass, please remember to use  use pip install libsass instead of pip install sass")


def sass_minify(css, settings: dict):
    """Minify SASS main function."""
    if have_sass:
        css = sass.compile(string=css)
    css = css_minify(css=css, settings=settings)
    return css
