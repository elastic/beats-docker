import pytest


class Beat:
    def __init__(self, name, process, binary_file, config_file):
        self.name = name
        self.process = process
        self.binary_file = binary_file
        self.config_file = config_file


@pytest.fixture()
def beat(Process, File, TestinfraBackend):
    # We name the container after the Beat, so asking for the hostname
    # lets us know which Beat we are testing.
    beat_name = TestinfraBackend.get_hostname()
    return Beat(
        name=beat_name,
        process=Process.get(comm=beat_name),
        binary_file=File('/usr/share/%s/%s' % (beat_name, beat_name)),
        config_file=File('/usr/share/%s/%s.yml' % (beat_name, beat_name))
    )
