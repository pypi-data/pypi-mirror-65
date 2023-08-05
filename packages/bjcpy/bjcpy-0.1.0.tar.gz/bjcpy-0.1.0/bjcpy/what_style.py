from .fits_style import fits_style
from .all_styles import all_styles

def what_style(beer):
    """Return a list of styles that a given beer fits into.
    
    Keyword arguments:
    beer-- dictionary representing the vital stats of the target beer
    """

    styles = all_styles()
    matching_styles = []

    for style in styles:
        searcheable_style = str(style)
        if fits_style(beer, searcheable_style):
            matching_styles.append(style)
        else:
            continue

    return matching_styles
