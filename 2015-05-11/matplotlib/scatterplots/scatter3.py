import sys
import os
import csv
import matplotlib.pyplot as plt
import math

def main(args):
    """
    Scatter plot of bolts UCI dataset
    """
    if len(args) > 0:
        fname = args[0]
    else:
        fname = "." + os.sep + "bolts.csv"
    data = []
    labels = []
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
                for i in xrange(len(row)):
                    data.append([])
                    labels.append(row[i])
                continue
            for i in xrange(len(row)):
                data[i].append(float(row[i]))

    fig = plt.figure()
    for x in xrange(len(data)):
        for y in xrange(len(data)):
            ax = fig.add_subplot(len(data), len(data), x * len(data) + y + 1)
            ax.scatter(data[x], data[y], alpha=0.5)
            ax.set_xlabel(labels[x])
            ax.set_ylabel(labels[y])
            ax.get_yaxis().set_ticklabels([])
            ax.get_xaxis().set_ticklabels([])
            ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="0.3")
            ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
    

