import os
import gzip
import re
import csv
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier, Evaluation
from weka.filters import Filter
from weka.core.classes import Random

# the directory with archives and output
directory = "/home/fracpete/temp/list"

# open csv file for writing
csvfilename = directory + "/emails.csv"
csvfile = open(csvfilename, "w")
fieldnames = ["content", "email"]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
writer.writeheader()

# loop through files
for filename in os.listdir(directory):
    if not filename.endswith(".txt.gz"):
        continue
    print(filename)
    
    # load mail archive
    f = gzip.open(filename, "r")
    content = f.read()
    f.close()

    # split archive into separate emails
    parts_pattern = re.compile("From .*")
    parts = parts_pattern.split(content)
    count = 0
    for part in parts:
        row = {}
        count += 1
        part_name = filename + "-" + str(count)
        print(part_name)

        # content
        content = part.strip()

        # email
        lines = content.split("\n")
        pattern = re.compile("From: .*")
        emails = []
        clean_content = []
        for line in lines:
            line = line.replace(",", " ").replace("\"", " ").replace("'", " ")
            if pattern.match(line):
                line = line.replace("From: ", "").strip()
                if len(line) > 0:
                    emails.append(line)
            elif len(line) > 0:
                clean_content.append(line)
        email = " ".join(emails)
        row["email"] = email
        row["content"] = " ".join(clean_content)
        len_email = len(row["email"])
        len_content = len(row["content"])
        if len_email > 0:
            print("  " + email)

        if (len_email > 0) and (len_content > 0):
            writer.writerow(row)

# close csvfile
csvfile.close()

# start JVM
jvm.start()

# load CSV file
loader = Loader(classname="weka.core.converters.CSVLoader", options=["-E", '"', "-F", ","])
data = loader.load_file(csvfilename)
#print(data)

# convert class to nominal
wfilter = Filter(classname="weka.filters.unsupervised.attribute.StringToNominal", options=["-R", "last"])
wfilter.set_inputformat(data)
data = wfilter.filter(data)

# convert content to string
wfilter = Filter(classname="weka.filters.unsupervised.attribute.NominalToString", options=["-C", "first"])
wfilter.set_inputformat(data)
data = wfilter.filter(data)

# set class attribute
data.set_class_index(data.num_attributes() - 1)

# generate baseline
zeror = Classifier(classname="weka.classifiers.rules.ZeroR")
evaluation = Evaluation(data)
evaluation.crossvalidate_model(zeror, data, 10, Random(1))
print("\nBaseline:\n" + evaluation.to_summary())

# perform text mining
j48 = Classifier(classname="weka.classifiers.trees.J48")
stwv = Filter(
    classname="weka.filters.unsupervised.attribute.StringToWordVector",
    options=["-R", "1", "-P", "att-"])
stwv.set_inputformat(data)
data = stwv.filter(data)
evaluation = Evaluation(data)
evaluation.crossvalidate_model(j48, data, 10, Random(1))
print("\nJ48:\n" + evaluation.to_summary())

# stop JVM
jvm.stop()