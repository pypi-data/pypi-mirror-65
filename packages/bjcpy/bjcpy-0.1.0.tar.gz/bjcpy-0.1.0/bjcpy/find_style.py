from .all_styles import all_styles

def find_style(term):
    """Return a list of styles the names of which include a search term.
    
    Keyword arguments:
    term-- a string to search
    """

    styles = all_styles()
    found_styles = []

    if term =='':
        return found_styles
    else:
        for style in styles:
            if term in style:
                found_styles.append(style)
            else:
                continue

        return found_styles
