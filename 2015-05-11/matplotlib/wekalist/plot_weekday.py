import sys
import os
import csv
import datetime
import time
import matplotlib.pyplot as plt
from numpy import linspace,exp
from numpy.random import randn
from scipy.interpolate import UnivariateSpline

def main(args):
    """
    Plots the counts per day of week.
    """
    counts = {}
    if len(args) > 0:
        fname = args[0]
    else:
        fname = "." + os.sep + "raw.csv"
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            struct = time.strptime(row[0], "%Y-%m-%d")
            wd = struct[6]
            if not wd in counts:
                counts[wd] = 0
            counts[wd] = counts[wd] + 1
    wdays = counts.keys()
    wdays.sort()
    scounts = []
    for wd in wdays:
        scounts.append(counts[wd])
    fig, ax = plt.subplots()
    ax.set_title('Wekalist - posts per day of week')
    ax.set_xlabel('Day of Week (Monday = 0)')
    ax.set_ylabel('Counts')
    ax.bar(wdays, scounts, 0.35)
    ax.autoscale_view()
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
    

