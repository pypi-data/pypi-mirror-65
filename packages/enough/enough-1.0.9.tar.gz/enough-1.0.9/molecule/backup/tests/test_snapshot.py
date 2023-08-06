testinfra_hosts = ['bind-host']


def openstack(host, cmd):
    cmd = host.run(f"""
    . /usr/lib/backup/openrc.sh
    openstack $OS_INSECURE {cmd}
    """)
    print(cmd.stderr)
    assert 0 == cmd.rc
    return cmd.stdout


def expected_snapshots(host, count):
    assert count == openstack(
        host, "volume snapshot list -f value -c Name | grep -c test-backup-volume")


def test_snapshots(host):
    # we need --insecure during tests otherwise going back in time a few days
    # may invalidate some certificates and result in errors such as:
    # SSL exception connecting to
    #    https://auth.cloud.ovh.net/v2.0/tokens: [SSL: CERTIFICATE_VERIFY_FAILED]
    with host.sudo():
        cmd = host.run("echo export OS_INSECURE=--insecure >> /usr/lib/backup/openrc.sh")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
    openstack(host, "volume create --size 1 test-backup-volume")
    cmd = host.run("/etc/cron.daily/prune-volume-snapshots 0")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    try:
        with host.sudo():
            host.run("timedatectl set-ntp 0")
            cmd = host.run("""
            set -x
            date -s '-15 days'
            bash -x /etc/cron.daily/volume-snapshots
            date -s '-30 days'
            bash -x /etc/cron.daily/volume-snapshots
            """)
            host.run("timedatectl set-ntp 1")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        expected_snapshots(host, '2')
        host.run("bash -x /etc/cron.daily/prune-volume-snapshots 30")
        expected_snapshots(host, '1')
    finally:
        host.run("timedatectl set-ntp 1")
        host.run("bash -x /etc/cron.daily/prune-volume-snapshots 0")
        openstack(host, "volume delete test-backup-volume || true")
