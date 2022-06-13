import pandas as pd

df = pd.read_csv("./data/Dog.csv")

# unique values in the column
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.unique.html
print(df['Primary_Breed'].unique())

# how many unique values in the column
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nunique.html
print(df['Primary_Breed'].nunique())
