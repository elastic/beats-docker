import os
import pytest

beat = os.environ['BEAT']


@pytest.fixture()
def process(Process):
    return Process.get(comm=beat)


def test_process_is_pid_1(process):
    assert process.pid == 1


def test_process_is_running_as_the_correct_user(process):
    if beat == 'packetbeat':
        correct_user = 'root'
    else:
        correct_user = beat
    assert process.user == correct_user


def test_process_was_started_with_the_verbose_flag(process):
    assert '-v' in process['args']


def test_process_was_started_with_the_foreground_flag(process):
    assert '-e' in process['args']
