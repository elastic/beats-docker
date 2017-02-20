from ..fixtures import beat


def test_process_is_pid_1(beat):
    assert beat.process.pid == 1


def test_process_is_running_as_the_correct_user(beat):
    if beat.name == 'packetbeat':
        assert beat.process.user == 'root'
    else:
        assert beat.process.user == beat.name


def test_process_was_started_with_correct_dir_flags(beat):
    assert '-path.home %s' % beat.home_dir.path in beat.process.args
    assert '-path.data %s' % beat.data_dir.path in beat.process.args
    assert '-path.logs %s' % beat.log_dir.path in beat.process.args
    assert '-path.config %s' % beat.config_dir.path in beat.process.args


def test_process_was_started_with_the_foreground_flag(beat):
    assert '-e' in beat.process['args']


def test_extra_args_can_be_passed_in_the_environment(beat):
    # The 'canary' string we are looking for is specified in docker-compose.yml.
    assert 'extra_args_test_canary' in beat.process['args']
