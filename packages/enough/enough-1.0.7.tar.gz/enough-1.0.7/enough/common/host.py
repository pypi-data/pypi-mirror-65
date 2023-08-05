import os
from abc import ABC, abstractmethod
import shutil
import tempfile

from enough import settings
from enough.common import openstack, docker
from enough.common import tcp


class Host(ABC):

    @abstractmethod
    def create_or_update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def write_inventory(self):
        pass


class HostDocker(Host):

    class DockerInfrastructure(docker.Docker):

        def create_image(self):
            name = super().create_image()
            dockerfile = os.path.join(self.root, 'internal/data/infrastructure.dockerfile')
            with tempfile.TemporaryDirectory() as d:
                shutil.copy(f'{settings.CONFIG_DIR}/infrastructure_key.pub', d)
                return self._create_image(None,
                                          '--build-arg', f'IMAGE_NAME={name}',
                                          '-f', dockerfile, d)

        def get_compose_content(self):
            f = os.path.join(self.root, 'internal/data/infrastructure-docker-compose.yml')
            return self.replace_content(open(f).read())

    def __init__(self, **kwargs):
        self.args = kwargs
        self.d = HostDocker.DockerInfrastructure(**self.args)

    def create_or_update(self):
        self.d.create_network(self.args['domain'])
        self.d.name = self.args['name']
        port = self.d.get_public_port('22')
        if not port:
            port = tcp.free_port()
            self.args['port'] = port
            self.d = HostDocker.DockerInfrastructure(**self.args)
            self.d.create_or_update()
        return {
            'ipv4': self.d.get_ip(),
            'port': '22',
        }

    def delete(self):
        domain = self.args['domain']
        for id in self.d.docker.ps('--filter', f'label=enough={domain}', '-q', _iter=True):
            self.d.docker.rm('-f', id.strip())

    def write_inventory(self):
        pass


class HostOpenStack(Host):

    def __init__(self, **kwargs):
        self.args = kwargs

    def create_or_update(self):
        s = openstack.Stack(self.args['clouds'],
                            openstack.Heat.get_stack_definition(self.args['name']))
        s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
        return s.create_or_update()

    def delete(self):
        for name in self.args['name']:
            s = openstack.Stack(self.args['clouds'],
                                openstack.Heat.get_stack_definition(name))
            s.delete()

    def write_inventory(self):
        openstack.Heat(self.args['clouds']).write_inventory()


def host_factory(**kwargs):
    if kwargs['driver'] == 'openstack':
        return HostOpenStack(**kwargs)
    else:
        return HostDocker(**kwargs)
