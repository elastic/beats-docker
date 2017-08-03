from .fixtures import beat
from .helpers import run


def test_entrypoint_with_args(beat):
    cmd = run(beat, "-c %s -configtest" % beat.config_file.path)
    assert cmd.returncode == 0


def test_entrypoint_with_beat_subcommand(beat):
    cmd = run(beat, 'help')
    assert cmd.returncode == 0
    assert 'Usage:' in cmd.stdout.decode()
    assert beat.name in cmd.stdout.decode()


def test_entrypoint_with_beat_subcommand_and_longopt(beat):
    cmd = run(beat, 'setup --help')
    assert cmd.returncode == 0
    assert b'This command does initial setup' in cmd.stdout


def test_entrypoint_with_abitrary_command(beat):
    cmd = run(beat, "echo Hello World!")
    assert cmd.returncode == 0
    assert cmd.stdout == b'Hello World!'


def test_entrypoint_with_explicit_beat_binary(beat):
    cmd = run(beat, '%s --version' % beat.name)
    assert cmd.returncode == 0
    assert beat.version in cmd.stdout.decode()
