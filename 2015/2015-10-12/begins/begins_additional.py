import begin

@begin.start
def yo(blah="b", something="s", *additional):
    print("blah: " + blah)
    print("something: " + something)
    print("additional: " + str(additional))

