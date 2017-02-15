import os

beat = os.environ['BEAT']


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
