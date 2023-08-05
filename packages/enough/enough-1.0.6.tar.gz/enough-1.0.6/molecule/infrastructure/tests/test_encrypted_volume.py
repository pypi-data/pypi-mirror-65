testinfra_hosts = ['cloud-host']


def test_encrypted_volume(host):
    cmd = host.run("""
    set -xe
    test -e /dev/mapper/spare
    grep -q /opt /etc/fstab
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
