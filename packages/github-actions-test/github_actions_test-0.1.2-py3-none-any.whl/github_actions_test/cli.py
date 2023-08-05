"""Console script for github_actions_test."""
import sys

import cleo

from . import __version__


class HelloCommand(cleo.Command):
    """
    First Command

    hello
    """

    def handle(self):
        self.line(
            "Replace this message by putting your code into "
            "github_actions_test.cli.main)"
        )
        self.line("See cleo documentation at https://cleo.readthedocs.io/en/latest/")


class Application(cleo.Application):
    def __init__(self):
        super().__init__("Github Actions Test", __version__)

        self.add(HelloCommand())


def main(args=None):
    return Application().run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
