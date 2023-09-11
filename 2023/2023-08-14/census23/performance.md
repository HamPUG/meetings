
## Apply
The use of `apply()` should be avoided in favour of vector methods. Where the complexity of the specification makes the implementation using vector methods difficult, performance issues can be mitigated by minimising the rows that the function is applied to. For example splitting the dataframe so `apply()` is only used against the smallest possible subset of a dataframe.

## Groupby

From the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html">documentation</a>:
>sort bool, default True
>
>Sort group keys. Get better performance by turning this off. Note this does not influence the order of observations within each group. Groupby preserves the order of rows within each group.


## Sorting
Sorting strings takes longer than sorting numbers so for large datasets it can be useful to first convert columns to numbers if the contents are known numeric. Converting the 2m+ row SLR (Statistics Location Register) table to numeric before sorting reduced sort time by more than half. 

## np.where(condition, x, y)
Be aware that `np.where()` will evaluate both the true and false values x and y regardless of the value of `condition`. Typically, complex arithmetic should be avoided.


## Generators

When accumulating potentially large amounts of data, using a generator can reduce the impact on resources. For example, creating a list of dataframes for use in a later `pd.concat()` will create all the dataframes before calling `pd.concat()`.

Use a generator instead. The result of each call to `prepare_files_for_household_size()` is lazy evaluated and is concated to `combined_df` without first creating the all the dataframes:

```python
to_concat = (self.prepare_files_for_household_size(n, hhld_data) for n in household_sizes)
combined_df = pd.concat(to_concat).reset_index()
```

## Record Linking

If you use the recordlinkage library be very careful not to mistake this:

```python
indexer = rl.Index()
indexer.block(on='A')
indexer.block(on='B')
links = indexer.index(table_1)
```

for this:

```python
indexer = rl.Index()
indexer.block(on=['A', 'B'])
links = indexer.index(table_1)
```

The first will block by variable 'A' and then add a second block by variable 'B' vs the second which will block by 'A and B'. Details aside, the first will explode memory on a large data set due to the quadratric nature of this type of linking where the second will try to 'reduce' the number of pairs that need comparison.


## Be Wary of isin(), use Joins

Imagine you have two tables and you want to know if there exists a value for column A from table 1 in column B of table 2.

The easiest way to do this is something like:

```python
linked = table_1[table_1['A'].isin(table_2['B'])]
```

But consider what happens as the size of table 2 grows. This will essentially do a look-up in table 2 for every item in table 1. If table 2 has 10 items it is no worries, but if it has 1_000_000 then we have to find a single item in table 2 for every item in table 1.

The solution is to use a join.

```python
linked = table_1.merge(table_2, how='inner', left_on='A', right_on='B')
```

The inner join will keep only records where there is a match in table 2.

## Avoid lambda's in loc[]
Using a lamda in a loc[] statement is unnecessary and has similar performance implications to `appy()`, i.e. the condition is applied individually to each row in the dataframe. 
