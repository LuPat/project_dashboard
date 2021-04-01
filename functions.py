import pandas as pd


def pre_cleaning(data):
    '''
    lower incoming columns, drop not needed columns and rename processed columns
    '''
    data.columns = map(str.lower, data.columns)
    data.drop(['vp: design parent'], axis=1, inplace=True)
    data.rename(columns={'vp: production plant': 'plant',
                         'vp: manufacturer group': 'customer',
                         'vp: country': 'country',
                         'vp: region': 'region'}, inplace=True)
    return data


def cars_wide_to_long(data):
    '''
    change dataset wide to long with a melt function
    '''
    data = data.melt(id_vars=['plant', 'country', 'region', 'customer'],
                     var_name='date',
                     value_name='carbuilds')
    return data


def clean_datetime(data):
    '''
    clean datetime columns
    '''
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month_name()
    move_date = data['date']
    move_month = data['month']
    move_year = data['year']
    data.drop(labels=['month'], axis=1, inplace=True)
    data.drop(labels=['date'], axis=1, inplace=True)
    data.drop(labels=['year'], axis=1, inplace=True)
    data.insert(0, 'month', move_month)
    data.insert(0, 'year', move_year)
    data.insert(0, 'date', move_date)
    data.index = data['year']
    return data

# add if statement to avoid auto call of function after import
# SEE YOUTUBE timeline‚
