import os
import pytest


class Beat:
    def __init__(self, name, process, home_dir, data_dir, config_dir, log_dir,
                 binary_file, config_file):
        self.name = name
        self.process = process
        self.home_dir = home_dir
        self.data_dir = data_dir
        self.config_dir = config_dir
        self.log_dir = log_dir
        self.binary_file = binary_file
        self.config_file = config_file
        try:
            self.version = os.environ['ELASTIC_VERSION']
        except KeyError:
            self.version = open('version.txt').read().strip()


@pytest.fixture()
def beat(Process, File, TestinfraBackend):
    # We name the container after the Beat, so asking for the hostname
    # lets us know which Beat we are testing.
    beat_name = TestinfraBackend.get_hostname()
    beat_home = '/usr/share/%s' % beat_name
    return Beat(
        name=beat_name,
        process=Process.get(comm=beat_name),
        home_dir=File(beat_home),
        data_dir=File('/var/lib/%s' % (beat_name)),
        config_dir=File('/etc/%s' % beat_name),
        log_dir=File('/var/log/%s' % (beat_name)),
        config_file=File('/etc/%s/%s.yml' % (beat_name, beat_name)),
        binary_file=File('%s/%s' % (beat_home, beat_name)),
    )
