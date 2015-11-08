"""
Extracts the raw data from the mbox files and generates a single CSV file.
"""

import sys
import os
import mailbox
import email.utils
import csv
import gzip
import time


def main(args):
    """
    Parses the .txt or .txt.gz mbox files in the specific directory.
    If not directory specific, cwd is used.
    """

    if len(args) > 0:
        mboxdir = args[0]
    else:
        mboxdir = "."
    print(mboxdir)

    with open("." + os.sep + "raw.csv", 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["date", "time", "subject"])
        for i in os.listdir(mboxdir):
            print("--> " + i)
            if i.endswith(".txt") or i.endswith(".txt.gz"):
                mboxfile = mboxdir + os.sep + i
                # decompress?
                if i.endswith(".txt"):
                    uncompressed = mboxfile
                    remove = False
                else:
                    f = gzip.open(mboxfile, 'rb')
                    file_content = f.read()
                    f.close()
                    uncompressed = mboxdir + os.sep + "current.txt"
                    f = open(uncompressed, 'wb')
                    f.write(file_content)
                    f.close()
                    remove = True
                # read emails
                emls = mailbox.mbox(uncompressed)
                print("--> " + str(len(emls)))
                for eml in emls:
                    if eml["date"] is not None:
                        ts = email.utils.parsedate(eml["date"])
                        datestr = time.strftime("%Y-%m-%d", ts)
                        timestr = time.strftime("%H:%M:%S", ts)
                        subject = eml["subject"].replace("[Wekalist] ", "")
                        subject = subject.replace("\n", " ").replace("\r", " ")
                        writer.writerow([datestr, timestr, subject])
                # clean up
                if remove:
                    os.remove(uncompressed)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print(ex)
    
