import os
import pytest

beat = os.environ['BEAT']

@pytest.fixture()
def beat_process(Process):
    return Process.get(comm=beat)


def test_beat_process(beat_process):
    assert beat_process.pid == 1


def test_process_is_running_as_the_correct_user(beat_process):
    if beat == 'packetbeat':
        correct_user = 'root'
    else:
        correct_user = beat
    assert beat_process.user == correct_user
