import logging
import os
import re
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from enough.version import __version__

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enough.settings')


class EnoughApp(App):

    def __init__(self, modules):
        super().__init__(
            description='enough',
            version=__version__,
            command_manager=CommandManager(modules),
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

    @staticmethod
    def remap_dot_enough(argv):
        home = os.path.expanduser('~/.enough')

        def remap(s):
            s = re.sub(r'^/\S+/.enough', home, s)
            s = re.sub(r'=/\S+/.enough', f'={home}', s)
            return s
        return [remap(a) for a in argv]

    @staticmethod
    def is_root():
        return os.geteuid() == 0

    @staticmethod
    def preserve_ownership():
        uid = os.geteuid()
        home = os.path.expanduser('~/.enough')
        if not uid == 0 or not os.path.exists(home):
            return False
        home_uid = os.stat(home).st_uid
        if uid != home_uid:
            os.system(f'chown -R {home_uid} {home}')
        return True

    def run(self, argv):
        r = super().run(EnoughApp.remap_dot_enough(argv))
        EnoughApp.preserve_ownership()
        return r


def main(argv=sys.argv[1:]):
    myapp = EnoughApp('enough.cli')
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
