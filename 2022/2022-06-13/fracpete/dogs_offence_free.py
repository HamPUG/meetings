import pandas as pd

df = pd.read_csv("./data/Dog.csv")

# group by flag
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
counts = df.groupby(['Primary_Breed', 'Offence_Free_Flag']).count()
counts = pd.DataFrame(counts['FID'])
counts = counts.rename(columns={'FID': 'Count'})
counts.reset_index(inplace=True)

# pivot, N/U/Y as separate columns
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html
counts = counts.pivot(index='Primary_Breed', columns='Offence_Free_Flag', values='Count')

# fill missing cells with 0
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
counts = counts.fillna(0)

# add column with percentage of known offences
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
counts['Offence %'] = counts.apply(
    lambda row: row.N / (row.Y + row.U + row.N) * 100.0, axis=1)

# sort by Offence %
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
counts = counts.sort_values(by=['Offence %'], ascending=False)

# save to CSV
counts.to_csv('./output/dog_offence.csv')
