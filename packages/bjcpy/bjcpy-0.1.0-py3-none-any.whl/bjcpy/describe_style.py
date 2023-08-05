from .style_data import dict_of_styles


def describe_style(style):
    """Return human readable dictionary of the vital stats for a beer style.
    
    Keyword arguments:
    style-- string indicating the name of the beer style
    """

    # Divide by 1000 to output floats instead of integers
    min_OG = dict_of_styles[style]['OG'][0]/1000
    max_OG = dict_of_styles[style]['OG'][-1]/1000
    min_FG = dict_of_styles[style]['FG'][0]/1000
    max_FG = dict_of_styles[style]['FG'][-1]/1000
    min_ABV = dict_of_styles[style]['ABV'][0]/1000
    max_ABV = dict_of_styles[style]['ABV'][-1]/1000
    min_IBU = dict_of_styles[style]['IBU'][0]/1000
    max_IBU = dict_of_styles[style]['IBU'][-1]/1000
    min_SRM = dict_of_styles[style]['SRM'][0]/1000
    max_SRM = dict_of_styles[style]['SRM'][-1]/1000

    characteristics={
        'Minimum OG': min_OG,
        'Maximum OG': max_OG,
        'Minimum FG': min_FG,
        'Maximum FG': max_FG,
        'Minimum ABV': min_ABV,
        'Maximum ABV': max_ABV,
        'Minimum IBU': min_IBU,
        'Maximum IBU': max_IBU,
        'Minimum SRM': min_SRM,
        'Maximum SRM': max_SRM
    }

    return characteristics


