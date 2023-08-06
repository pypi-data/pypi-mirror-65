import os

from enough import cmd


def test_create(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert cmd.main(['create']) == 0
    out, err = capsys.readouterr()
    assert 'OK' in out


def test_playbook(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.ansible_utils.Playbook.run',
                 side_effect=lambda: print('PLAYBOOK'))
    assert cmd.main(['playbook']) == 0
    out, err = capsys.readouterr()
    assert 'PLAYBOOK' in out


def test_remap_dot_enough():
    p = '.enough/thing'
    unchanged = '/foo/bar/'
    expected = [f'{os.path.expanduser("~")}/{p}', unchanged]
    assert cmd.EnoughApp.remap_dot_enough([f'/home/user/{p}', unchanged]) == expected
    expected = [f'--option={os.path.expanduser("~")}/{p}', unchanged]
    assert cmd.EnoughApp.remap_dot_enough([f'--option=/home/user/{p}', unchanged]) == expected


def test_preserve_ownership(mocker, tmpdir):
    #
    # not running as root, do nothing
    #
    assert cmd.EnoughApp.preserve_ownership() is False

    #
    # pretend to run as root and chown to self
    #
    mocker.patch('os.geteuid', return_value=0)
    mocker.patch('os.path.expanduser', return_value=str(tmpdir))
    assert cmd.EnoughApp.preserve_ownership() is True
