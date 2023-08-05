from enough.cmd import main


def test_create(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['create']) == 0
    out, err = capsys.readouterr()
    assert 'OK' in out


def test_playbook(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.ansible_utils.Playbook.run',
                 side_effect=lambda: print('PLAYBOOK'))
    assert main(['playbook']) == 0
    out, err = capsys.readouterr()
    assert 'PLAYBOOK' in out
