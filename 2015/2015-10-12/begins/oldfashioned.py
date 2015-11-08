import sys

def yo(blah, something):
    print("blah: " + blah)
    print("something: " + something)

if __name__ == '__main__':
    param1 = "b"
    param2 = "s"
    params = sys.argv[1:]
    for index, arg in enumerate(params):
        print(str(index) + ": " + arg)
        if arg == "-b":
            param1 = params[index + 1]
        elif arg == "-s":
            param2 = params[index + 1]
    yo(param1, param2)

