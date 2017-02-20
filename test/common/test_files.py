from ..fixtures import beat
import os


def test_binary_file_version(Command, beat):
    version_string = '%s version %s (amd64), libbeat %s' \
                     % (beat.name, beat.version, beat.version)
    command = Command('%s --version' % beat.binary_file.path)
    assert command.stdout.strip() == version_string


def test_binary_file_permissions(beat):
    assert beat.binary_file.user == 'root'
    assert beat.binary_file.group == beat.name
    assert beat.binary_file.mode == 0o0750


def test_script_file_permissions(File, Command, beat):
    script_paths = Command.check_output('find %s/scripts/' % beat.home_dir.path).strip().split()
    for path in script_paths:
        script = File(path)
        assert script.user == 'root'
        assert script.group == beat.name
        assert script.mode == 0o0750


def test_config_file_permissions(beat):
    assert beat.config_file.user == 'root'
    assert beat.config_file.group == beat.name
    assert beat.config_file.mode == 0o0640


def test_config_dir_permissions(beat):
    assert beat.config_dir.user == 'root'
    assert beat.config_dir.group == beat.name
    assert beat.config_dir.mode == 0o0750


def test_data_dir_permissions(beat):
    assert beat.data_dir.user == 'root'
    assert beat.data_dir.group == beat.name
    assert beat.data_dir.mode == 0o0770


def test_log_dir_permissions(beat):
    assert beat.log_dir.user == 'root'
    assert beat.log_dir.group == beat.name
    assert beat.log_dir.mode == 0o0770


def test_dashboard_archive_is_present(File, beat):
    archive = File('%s/beats-dashboards-%s.zip' % (beat.home_dir.path, beat.version))
    assert archive.exists


def test_template_locations(File, beat):
    template_names = [
        '%s.template.json' % beat.name,
        '%s.template-es2x.json' % beat.name
    ]
    for name in template_names:
        template = File('%s/%s' % (beat.home_dir.path, name))
        symlink = File('%s/%s' % (beat.config_dir.path, name))
        assert template.exists
        assert symlink.linked_to == template.path
