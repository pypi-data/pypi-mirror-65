from .scour import scourString


def svg_minify(svg, settings: dict):
    """Minify SVG main function."""
    svg = scourString(in_string=svg, options=settings)
    return svg
