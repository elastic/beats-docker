from .fixtures import beat


def test_config_file_passes_config_test(Command, beat):
    configtest = '%s -c %s -configtest' % (beat.binary_file.path, beat.config_file.path)
    Command.run_expect([0], configtest)
