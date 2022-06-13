import pandas as pd

df = pd.read_csv("./data/Dog.csv")
total_dist = df['Primary_Breed'].value_counts()

suburbs = list(df['Kept_At_Suburb'].unique())
columns = []
for suburb in suburbs:
    # skip missing value
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.isna.html
    if pd.isna(suburb):
        continue
    print(suburb)
    # get subset for suburb
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
    df_sub = df.loc[df['Kept_At_Suburb'] == suburb]
    sub_dist = df_sub['Primary_Breed'].value_counts()
    # align total distribution with suburb distribution
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.align.html
    l, r = total_dist.align(sub_dist, join="outer", axis=0, fill_value=0)
    if len(columns) == 0:
        # turn Series into DataFrame
        l = pd.DataFrame(l)
        # rename column
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
        l = l.rename(columns={'Primary_Breed': 'Total'})
        columns.append(l)
    r = pd.DataFrame(r)
    r = r.rename(columns={'Primary_Breed': suburb})
    columns.append(r)

# combine the distributions
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html
dists = pd.concat(columns, axis=1)
dists.to_csv("./output/dogs_suburb_dist.csv")
