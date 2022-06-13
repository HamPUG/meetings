import pandas as pd
import matplotlib.pyplot as plt

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
df = pd.read_csv("./data/Dog.csv")

# how many occurrences per value in the column
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html
dist = df['Primary_Breed'].value_counts()
print(dist)

# push the data into matplotlib (default plot backend)
dist.plot()

if False:
    # customize the plot
    plt.xticks(rotation=90)  # rotate labels by 90deg
    plt.tight_layout()  # to avoid labels cut off
    plt.locator_params(axis='y', nbins=10)  # for numeric axis how many tick "bins" to use

    # for strings we need to define our own positions (ticks) and the corresponding labels
    xlabels = list(dist.index[0::10])
    xticks = [x for x in range(0, len(dist.index), 10)]
    plt.xticks(ticks=xticks, labels=xlabels)

# save/display the plot
plt.savefig("./output/dogs_breed_dist.png")
plt.show()

# Troubleshooting:
# UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
# sudo apt-get install python3-tk
