import argparse
from cliff.command import Command

from enough.common import ansible_utils


class Playbook(Command):
    "Playbook"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('args', nargs=argparse.REMAINDER)
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        playbook = ansible_utils.Playbook(**args)
        playbook.run()
