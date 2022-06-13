import dask.dataframe as dd

# lazy loading using dask's DataFrame
# https://docs.dask.org/en/stable/generated/dask.dataframe.read_csv.html
df = dd.read_csv("./data/Fleet30Nov2017.csv", encoding='latin-1', dtype={'ALTERNATIVE_MOTIVE_POWER': 'object',
                                                                         'FIRST_NZ_REGISTRATION_MONTH': 'float64',
                                                                         'FIRST_NZ_REGISTRATION_YEAR': 'float64'})
# get subset of only private vehicles, built in 2000 or newer
df = df[(df['INDUSTRY_CLASS'] == 'PRIVATE') & (df['VEHICLE_YEAR'] >= 2000)]

# materialize data, ie apply operations
# https://docs.dask.org/en/stable/generated/dask.dataframe.DataFrame.compute.html#dask.dataframe.DataFrame.compute
df = df.compute()
print("rows/cols\n", df.shape)
print("column names\n", df.columns)

# save to disk
df.to_csv("./data/Fleet30Nov2017_private2000.csv")
