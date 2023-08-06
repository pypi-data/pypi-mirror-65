import sys

from enough import cmd


def main(argv=sys.argv[1:]):
    myapp = cmd.EnoughApp('enough.internal.cli')
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
