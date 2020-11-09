import argparse
import traceback
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def main(args=None):
    """
    The main method for parsing command-line arguments and running the application.
    The matplotlib code taken from here:
    https://matplotlib.org/3.1.1/gallery/pyplots/text_layout.html#sphx-glr-gallery-pyplots-text-layout-py

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="the text to output", required=True)
    parsed = parser.parse_args(args=args)

    # build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    # axes coordinates are 0,0 is bottom left and 1,1 is upper right
    p = patches.Rectangle(
        (left, bottom), width, height,
        fill=False, transform=ax.transAxes, clip_on=False)

    ax.add_patch(p)

    ax.text(0.5*(left+right), 0.5*(bottom+top), parsed.text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='red',
            transform=ax.transAxes)

    ax.set_axis_off()
    plt.show()

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

