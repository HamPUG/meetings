import argparse
import traceback
import numpy as np
from dbg.generate import generate


def main(args=None):
    """
    The main method for parsing command-line arguments and running the application.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="the text to output", required=True)
    parsed = parser.parse_args(args=args)

    generate(parsed.text, ps1="msdp", subtitle=np.version.full_version)

def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.
    :return: 0 for success, 1 for failure.
    :rtype: int
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    main()

