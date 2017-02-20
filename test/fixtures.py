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
    beat_home = os.path.join(os.sep, 'usr', 'share', beat_name)
    return Beat(
        name=beat_name,
        process=Process.get(comm=beat_name),
        home_dir=File(beat_home),
        data_dir=File(os.path.join(beat_home, 'data')),
        config_dir=File(beat_home),
        log_dir=File(os.path.join(beat_home, 'logs')),
        config_file=File(os.path.join(beat_home, '%s.yml' % beat_name)),
        binary_file=File(os.path.join(beat_home, beat_name)),
    )
