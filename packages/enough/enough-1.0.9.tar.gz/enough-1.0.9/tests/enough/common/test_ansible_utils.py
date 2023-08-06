from enough.common import ansible_utils
import json
import pytest
import shutil
import yaml


def test_parse_output():
    data = {"changed": False}
    output = '51.68.81.22 | SUCCESS => ' + json.dumps(data)
    assert ansible_utils.parse_output(output) == data


def test_get_variable():
    defaults = yaml.load(open('molecule/api/roles/api/defaults/main.yml'))
    variable = 'api_admin_password'
    value = ansible_utils.get_variable('api', variable, 'api-host')
    assert defaults[variable] == value


def test_playbook_roles_path():
    p = ansible_utils.Playbook()
    r = p.roles_path('.')
    assert '/infrastructure/' in r


def test_playbook_ensure_decrypted(tmpdir):
    p = ansible_utils.Playbook()
    shutil.copytree('tests/enough/common/test_ansible_utils/domain.com',
                    f'{tmpdir}/domain.com')
    c = f'{tmpdir}/domain.com'
    p.config_dir = c

    #
    # decryption is needed but no password is found
    #
    with pytest.raises(ansible_utils.Playbook.NoPasswordException):
        assert p.ensure_decrypted() is False
    shutil.copyfile('tests/enough/common/test_ansible_utils/domain.com.pass',
                    f'{tmpdir}/domain.com.pass')

    #
    # all files are decrypted
    #
    for f in p.encrypted_files(c):
        if f.endswith('not-encrypted.key'):
            continue
        assert p.is_encrypted(f)
    assert p.ensure_decrypted() is True
    for f in p.encrypted_files(c):
        assert not p.is_encrypted(f)
    #
    # nothing to do
    #
    assert p.ensure_decrypted() is False


def test_playbook_run_with_args(capsys, caplog):
    kwargs = {
        'args': ['--', 'tests/enough/common/test_ansible_utils/playbook-ok.yml'],
    }
    p = ansible_utils.Playbook(**kwargs)
    p.run()
    out, err = capsys.readouterr()
    assert 'OK_PLAYBOOK' in caplog.text
    assert 'OK_IMPORTED' in caplog.text


def test_playbook_run_no_args(mocker):
    called = {}

    def playbook():
        def run(*args):
            assert '--private-key' in args
            called['playbook'] = True
        return run
    mocker.patch('enough.common.ansible_utils.Playbook.bake',
                 side_effect=playbook)
    kwargs = {
        'args': [],
    }
    p = ansible_utils.Playbook(**kwargs)
    p.run()
    assert 'playbook' in called
