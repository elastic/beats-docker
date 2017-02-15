from ..fixtures import beat
import os

version = os.environ['ELASTIC_VERSION']


def test_binary_file_version(Command, beat):
    version_string = '%s version %s (amd64), libbeat %s' % (beat.name, version, version)
    assert Command('%s --version' % beat.name).stdout.strip() == version_string


def test_binary_file_permissions(File, beat):
    binary = File("/usr/share/%s/%s" % (beat.name, beat.name))
    assert binary.user == beat.name
    assert binary.group == beat.name
    assert binary.mode == 0o0755


def test_config_file_permissions(File, beat):
    config = File("/usr/share/%s/%s.yml" % (beat.name, beat.name))
    assert config.user == beat.name
    assert config.group == beat.name
    assert config.mode == 0o0600
