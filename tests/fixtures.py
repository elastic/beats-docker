import json
import os
import pytest
import datetime
from subprocess import run, PIPE

version = run('./bin/elastic-version', stdout=PIPE).stdout.decode().strip()


@pytest.fixture()
def beat(Process, File, TestinfraBackend, Command):
    class Beat:
        def __init__(self):
            # We name the container after the Beat, so asking for the hostname
            # lets us know which Beat we are testing.
            name = TestinfraBackend.get_hostname()
            self.name = name

            # Auditbeat might already be running on this system and in the top-level
            # PID namespace too. We can't just assume that the first Auditbeat process
            # we see is the one we are interested in. A better assumption is that the
            # _newest_ process is the one we are interested in.
            processes = {}
            for process in Process.filter(comm=name):
                start_time = datetime.datetime.strptime(process['lstart'], "%a %b %d %H:%M:%S %Y")
                processes[start_time] = process
            newest_process = processes[max(processes.keys())]
            self.process = newest_process

            home = os.path.join(os.sep, 'usr', 'share', name)
            self.home_dir = File(home)
            self.data_dir = File(os.path.join(home, 'data'))
            self.config_dir = File(home)
            self.log_dir = File(os.path.join(home, 'logs'))
            self.kibana_dir = File(os.path.join(home, 'kibana'))
            self.binary_file = File(os.path.join(home, name))
            self.config_file = File(os.path.join(home, '%s.yml' % name))
            self.version = version.replace('-SNAPSHOT', '')

            # What Linux capabilities does the binary file have?
            capability_string = Command.check_output('getcap %s' % self.binary_file.path)
            # Like: '/usr/share/packetbeat/packetbeat = cap_net_admin,cap_net_raw+eip'
            if capability_string:
                self.capabilities = capability_string.split()[-1].split('+')[0].split(',')
                # Like: ['cap_net_raw', 'cap_net_admin']
            else:
                self.capabilities = []

            if 'STAGING_BUILD_NUM' in os.environ:
                self.tag = '%s-%s' % (version, os.environ['STAGING_BUILD_NUM'])
            else:
                self.tag = version

            self.flavor = pytest.config.getoption('--image-flavor')
            if self.flavor != 'full':
                self.image = 'docker.elastic.co/beats/%s-%s:%s' % (self.name, self.flavor, self.tag)
            else:
                self.image = 'docker.elastic.co/beats/%s:%s' % (self.name, self.tag)

            self.docker_metadata = json.loads(
                run(['docker', 'inspect', self.image], stdout=PIPE).stdout.decode())[0]

    return Beat()
