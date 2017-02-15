import os

beat = os.environ['BEAT']
version = os.environ['ELASTIC_VERSION']


def test_binary_file_version(Command):
    version_string = '%s version %s (amd64), libbeat %s' % (beat, version, version)
    assert Command('%s --version' % beat).stdout.strip() == version_string


def test_binary_file_permissions(File):
    binary = File("/usr/share/%s/%s" % (beat, beat))
    assert binary.user == beat
    assert binary.group == beat
    assert binary.mode == 0o0755


def test_config_file_permissions(File):
    config = File("/usr/share/%s/%s.yml" % (beat, beat))
    assert config.user == beat
    assert config.group == beat
    assert config.mode == 0o0600
