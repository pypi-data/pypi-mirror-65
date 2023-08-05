from .all_styles import all_styles


def is_style(style):
    """Check if a style is included in the BJCP guidelines.
    
    Keyword arguments:
    style-- string naming a suspected style
    """

    styles = all_styles()
    if style in styles:
        return True
    else:
        return False
