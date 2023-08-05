from .style_data import dict_of_styles


def all_styles():
    """Return a list of every BJCP style"""
    
    return list(dict_of_styles.keys())
