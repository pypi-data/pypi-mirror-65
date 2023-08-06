import sys

from pyadr.cli.application import App
from pyadr.cli.config import LoggingAppConfig


def main(args=None):
    return App(config=LoggingAppConfig()).run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
