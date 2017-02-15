import pytest


class Beat:
    def __init__(self, name, process):
        self.name = name
        self.process = process


@pytest.fixture()
def beat(Process, TestinfraBackend):
    # We name the container after the Beat, so asking for the hostname
    # let's us know which Beat we are testing.
    beat_name = TestinfraBackend.get_hostname()
    print(beat_name)
    return Beat(name=beat_name, process=Process.get(comm=beat_name))
