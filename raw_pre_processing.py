import numpy as np
import pandas as pd
from functions import pre_cleaning, cars_wide_to_long

# Import data from Excel file 
df = pd.read_excel('./data/car_builds_ihs.xlsx', sheet_name='Data')

# Pre Clean Data and rename columns - see functions.py
df_cleaned = pre_cleaning(df)

# Save pre cleaned data in wide format
df_cleaned.to_csv('./data/car_builds_wide_format.csv')

# transform data wide to long format
df_long = cars_wide_to_long(df_cleaned)

# Save data in long format
df_long.to_csv('./data/car_builds_long_format.csv')

