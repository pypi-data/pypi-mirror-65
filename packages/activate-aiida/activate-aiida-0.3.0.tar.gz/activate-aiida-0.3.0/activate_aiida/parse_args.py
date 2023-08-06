import argparse
import sys

from activate_aiida import __version__


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter,
):
    pass


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)

    def print_usage(self, file=None):
        if file is None:
            file = sys.stderr
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = sys.stderr
        self._print_message(self.format_help(), file)


def get_parser(**kwargs):
    return CustomParser(formatter_class=CustomFormatter, **kwargs)


def run(sys_args=None):

    if sys_args is None:
        sys_args = sys.argv[1:]

    parser = get_parser(
        description=("initialises an aiida environment via yaml config file")
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "filepath",
        type=str,
        nargs="?",
        help="path to config file",
        metavar="filepath",
        default="aiida_config.yaml",
    )
    parser.add_argument(
        "-c",
        "--create-db",
        action="store_true",
        help=("if the database or aiida profile " "do not exist then create them"),
    )
    parser.add_argument(
        "-w",
        "--daemon-workers",
        type=int,
        default=0,
        help=("If >0, start the daemon with this many workers"),
    )

    args = parser.parse_args(sys_args)
    options = vars(args)
    sys.stdout.write(
        "{0},{1},{2}".format(
            options["filepath"], options["create_db"], options["daemon_workers"]
        )
    )
