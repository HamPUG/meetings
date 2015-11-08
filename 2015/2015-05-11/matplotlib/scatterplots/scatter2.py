import sys
import os
import csv
import matplotlib.pyplot as plt
import math

def main(args):
    """
    Scatter plot of slug length vs weight
    """
    if len(args) > 0:
        fname = args[0]
    else:
        fname = "." + os.sep + "slug.csv"
    length = []
    weight = []
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            length.append(math.log(float(row[0])))
            weight.append(math.log(float(row[1])))
    fig, ax = plt.subplots()
    ax.set_title('Slugs')
    ax.set_xlabel('log(length)')
    ax.set_ylabel('log(weight)')
    ax.scatter(length, weight)
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
    

