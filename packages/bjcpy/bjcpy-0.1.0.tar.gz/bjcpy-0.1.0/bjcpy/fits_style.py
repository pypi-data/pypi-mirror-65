import random
from .style_data import dict_of_styles


def fits_style(beer, style):
    """Check that a target beer adheres to a certain style, returning 
    True if beer fits and False otherwise.
    
    Keyword arguments:
    beer-- dictionary representing the vital stats of the target beer
    style-- string indicating the style we want to check that the target beer fits into
    """
    for key in beer:
        if key not in dict_of_styles[style]:
            raise KeyError
        else:
            if type(beer.get('OG')) == str or type(beer.get('FG')) == str or type(beer.get('ABV')) == str \
            or type(beer.get('IBU')) == str or type(beer.get('SRM')) == str:
                raise TypeError
            else:

                # Convert the beer's vital stats to integers to avoid issues with floats and/or fill in missing info.
                if beer.get('OG') == None and beer.get('FG') == None and beer.get('ABV') == None \
                and beer.get('IBU') == None and beer.get('SRM') == None:
                    return False
                else:
                    if beer.get('OG') == None:
                        new_OG = random.choice(dict_of_styles[style]['OG'])
                    else:
                        new_OG = beer['OG']*1000
                    if beer.get('FG') == None:
                        new_FG = random.choice(dict_of_styles[style]['FG'])
                    else:
                        new_FG = beer['FG']*1000
                    if beer.get('ABV') == None:
                        new_ABV = random.choice(dict_of_styles[style]['ABV'])
                    else:
                        new_ABV = beer['ABV']*1000
                    if beer.get('IBU') == None:
                        new_IBU = random.choice(dict_of_styles[style]['IBU'])
                    else:
                        new_IBU = beer['IBU']*1000
                    if beer.get('SRM') == None:
                        new_SRM = random.choice(dict_of_styles[style]['SRM'])
                    else:
                        new_SRM = beer['SRM']*1000

                # Check that the resulting stats are in range
                    if new_OG in dict_of_styles[style]['OG'] and new_FG in dict_of_styles[style]['FG'] \
                    and new_ABV in dict_of_styles[style]['ABV'] and new_IBU in dict_of_styles[style]['IBU'] \
                    and new_SRM in dict_of_styles[style]['SRM']:
                        return True
                    else:
                        return False
