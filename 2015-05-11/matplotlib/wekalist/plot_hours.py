import sys
import os
import csv
import datetime
import time
import matplotlib.pyplot as plt

def main(args):
    """
    Plots the counts per hour.
    """
    counts = {}
    helpcounts = {}
    howcounts = {}
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
            struct = time.strptime(row[1], "%H:%M:%S")
            h = struct[3]
            if not h in counts:
                counts[h] = 0
            counts[h] = counts[h] + 1
            subject = row[2].lower()
            if not h in helpcounts:
                helpcounts[h] = 0
            if not h in howcounts:
                howcounts[h] = 0
            # help in subject?
            if subject.find("help") > -1:
                helpcounts[h] = helpcounts[h] + 1
            # how in subject?
            if subject.find("how") > -1:
                howcounts[h] = howcounts[h] + 1
    hours = counts.keys()
    hours.sort()
    scounts = []
    shelpcounts = []
    showcounts = []
    for h in hours:
        scounts.append(counts[h])
        shelpcounts.append(helpcounts[h])
        showcounts.append(howcounts[h])
    fig, ax = plt.subplots()
    ax.set_title('Wekalist - posts per hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Counts')
    ax.plot(hours, scounts, "blue", label="All")
    ax.fill_between(hours, 0, scounts, facecolor='blue', alpha=0.5)
    ax.plot(hours, shelpcounts, "red", label="help?")
    ax.plot(hours, showcounts, "black", label="how?")
    ax.grid(True)
    legend = plt.legend(loc='upper right', shadow=True)
    fig.autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
    

