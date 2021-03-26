import pandas as pd

def pre_cleaning(data):
    '''
    lower incoming columns, drop not needed columns and rename processed columns
    '''
    data.columns = map(str.lower, data.columns)
    data.drop(['vp: design parent'], axis=1, inplace=True)
    data.rename(columns={'vp: production plant': 'plant',
                     'vp: manufacturer group' : 'customer',
                     'vp: country': 'country', 
                     'vp: region': 'region'}, inplace=True)
    return data

def cars_wide_to_long(data):
    '''
    change dataset wide to long with a melt function
    '''
    data = data.melt(id_vars = ['plant', 'country', 'region', 'customer'], 
              var_name = 'date', 
              value_name = 'carbuilds')
    return data

# add if statement to avoid auto call of function after import
# SEE YOUTUBE timeline‚