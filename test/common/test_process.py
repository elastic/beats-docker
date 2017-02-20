from ..fixtures import beat


def test_process_is_pid_1(beat):
    assert beat.process.pid == 1


def test_process_is_running_as_the_correct_user(beat):
    if beat.name == 'packetbeat':
        assert beat.process.user == 'root'
    else:
        assert beat.process.user == beat.name


def test_process_was_started_with_the_foreground_flag(beat):
    assert '-e' in beat.process['args']
