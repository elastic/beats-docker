from .fixtures import beat
from .helpers import run


def test_entrypoint_args(Command, beat):
    cmd = run(beat, "-c %s -configtest" % beat.config_file.path)
    assert cmd.returncode == 0


def test_entrypoint_command(Command, beat):
    cmd = run(beat, "echo Hello World!")
    assert cmd.returncode == 0
    assert cmd.stdout == b'Hello World!'
