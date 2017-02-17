from ..fixtures import beat
import os

try:
    version = os.environ['ELASTIC_VERSION']
except KeyError:
    version = open('version.txt').read().strip()


def test_binary_file_version(Command, beat):
    version_string = '%s version %s (amd64), libbeat %s' % (beat.name, version, version)
    command = Command('%s --version' % beat.binary_file.path)
    assert command.stdout.strip() == version_string


def test_binary_file_is_owned_by_root(beat):
    assert beat.binary_file.user == 'root'


def test_config_file_is_owned_by_root(beat):
    assert beat.config_file.user == 'root'


def test_binary_file_is_not_writable_by_the_beat_user(Command, beat):
    Command.run_expect([1], 'su -c "echo hax > %s" %s' %
                       (beat.binary_file.path, beat.name))


def test_config_file_is_not_writable_by_the_beat_user(Command, beat):
    Command.run_expect([1], 'su -c "echo hax > %s" %s' %
                       (beat.config_file.path, beat.name))


def test_config_file_mode(beat):
    assert beat.config_file.group == beat.name
    assert beat.config_file.mode == 0o0640
