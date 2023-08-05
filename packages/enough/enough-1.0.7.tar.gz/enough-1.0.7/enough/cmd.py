import logging
import os
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from enough.version import __version__

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enough.settings')


class EnoughApp(App):

    def __init__(self):
        super(EnoughApp, self).__init__(
            description='enough',
            version=__version__,
            command_manager=CommandManager('enough.cli'),
            deferred_help=True,
            )

    def configure_logging(self):
        super().configure_logging()

        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.WARNING)

        level = {0: logging.WARNING,
                 1: logging.INFO,
                 2: logging.DEBUG}.get(self.options.verbose_level, logging.DEBUG)

        root_logger = logging.getLogger('enough')
        root_logger.setLevel(level)

    def initialize_app(self, argv):
        os.environ['ENOUGH_DOMAIN'] = self.options.domain

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super().build_option_parser(description, version, argparse_kwargs)
        parser.add_argument('--domain', default='enough.community', help='Enough domain name')
        return parser


def main(argv=sys.argv[1:]):
    myapp = EnoughApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
