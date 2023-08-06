import glob
import json
import logging
import os
import re
import sh
import tempfile
import textwrap

from enough import settings

log = logging.getLogger(__name__)


def parse_output(output):
    json_result = re.sub(r'.*?=> ', '', output)
    return json.loads(json_result)


def bake_ansible_playbook():
    args = ['-i', 'inventory']
    if settings.CONFIG_DIR != '.':
        args.extend(['-i', f'{settings.CONFIG_DIR}/inventory'])
    return sh.ansible_playbook.bake(
        *args,
        _tee=True,
        _out=lambda x: log.info(x.strip()),
        _err=lambda x: log.info(x.strip()),
        _truncate_exc=False,
        _cwd=settings.SHARE_DIR,
        _env={'ANSIBLE_NOCOLOR': 'true'},
    )


def get_variable(role, variable, host):
    with tempfile.NamedTemporaryFile() as f:
        # the sourrounding "> <" are to prevent conversion to int, list or whatever
        playbook = textwrap.dedent("""
        ---
        - hosts: all
          gather_facts: false

          roles:
            - role: "{{ rolevar }}"

          tasks:
            - name: print variable
              debug:
                msg: ">{{ variable }}<"
        """)
        f.write(bytearray(playbook, 'utf-8'))
        f.flush()
        print(playbook)
        r = bake_ansible_playbook()(
            '-e', f'rolevar={role}',
            '-e', 'variable={{ ' + variable + ' }}',
            '--limit', host,
            '--start-at-task=print variable',
            f.name)
        m = re.search(r'"msg": ">(.*)<"$', r.stdout.decode('utf-8'), re.MULTILINE)
        return m.group(1)


class Playbook(object):

    class NoPasswordException(Exception):
        pass

    def __init__(self, **kwargs):
        self.args = kwargs
        self.share_dir = settings.SHARE_DIR
        self.config_dir = settings.CONFIG_DIR

    @staticmethod
    def is_encrypted(p):
        if not os.path.exists(p):
            return False
        c = open(p).read()
        return c.startswith('$ANSIBLE_VAULT')

    @staticmethod
    def encrypted_files(d):
        return [
            f'{d}/infrastructure_key',
            f'{d}/inventory/group_vars/all/clouds.yml',
        ] + glob.glob(f'{d}/certs/*.key')

    def ensure_decrypted(self):
        encrypted = [f for f in self.encrypted_files(self.config_dir)
                     if self.is_encrypted(f)]
        if len(encrypted) == 0:
            return False
        vault_password_option = self.vault_password_option()
        if not vault_password_option:
            raise Playbook.NoPasswordException(
                f'{encrypted} are encrypted but {self.config_dir}.pass does not exist')
        for f in encrypted:
            log.info(f'decrypt {f}')
            sh.ansible_vault.decrypt(
                vault_password_option,
                f,
                _tee=True,
                _out=lambda x: log.info(x.strip()),
                _err=lambda x: log.info(x.strip()),
                _truncate_exc=False,
                _env={
                    'ANSIBLE_NOCOLOR': 'true',
                }
            )
        return True

    def vault_password_option(self):
        password_file = f'{self.config_dir}.pass'
        if os.path.exists(password_file):
            return f'--vault-password-file={password_file}'
        else:
            log.info(f'no decryption because {password_file} does not exist')
            return None

    @staticmethod
    def roles_path(d):
        r = glob.glob(f'{d}/molecule/*/roles')
        r.append(f'{d}/molecule/wazuh/wazuh-ansible/roles/wazuh')
        return ":".join(r)

    def bake(self):
        args = [
            '-i', f'{self.share_dir}/inventory',
        ]
        if self.vault_password_option():
            args.append(self.vault_password_option())
        if self.share_dir != self.config_dir:
            args.extend(['-i', f'{self.config_dir}/inventory'])
        logger = logging.getLogger(__name__)
        return sh.ansible_playbook.bake(
            *args,
            _tee=True,
            _out=lambda x: logger.info(x.strip()),
            _err=lambda x: logger.info(x.strip()),
            _truncate_exc=False,
            _env={
                'SHARE_DIR': self.share_dir,
                'CONFIG_DIR': self.config_dir,
                'ANSIBLE_ROLES_PATH': self.roles_path(self.share_dir),
                'ANSIBLE_NOCOLOR': 'true',
            },
        )

    def run(self):
        self.ensure_decrypted()
        if not self.args['args']:
            args = [
                '--private-key', f'{self.config_dir}/infrastructure_key',
                f'{self.config_dir}/enough-playbook.yml'
            ]
        else:
            args = self.args['args'][1:]
        self.bake()(*args)
