# let's load a CSV file
import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
df = pd.read_csv("./data/Dog.csv")
print("rows/cols\n", df.shape)
print("column names\n", df.columns)
