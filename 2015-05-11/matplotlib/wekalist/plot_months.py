import sys
import os
import csv
import datetime
import time
import matplotlib.pyplot as plt

def main(args):
    """
    Plots the counts per month.
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
            t = time.mktime(struct)
            d = datetime.date(struct[0], struct[1], 1)
            if not d in counts:
                counts[d] = 0
            counts[d] = counts[d] + 1
    dates = counts.keys()
    dates.sort()
    scounts = []
    for d in dates:
        scounts.append(counts[d])
    fig, ax = plt.subplots()
    ax.set_title('Wekalist - posts per month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Counts')
    ax.plot_date(dates, scounts, '-')
    ax.autoscale_view()
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
    

