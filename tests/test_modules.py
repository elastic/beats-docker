from .fixtures import beat
import os

# Beats supporting modules command:
MODULES_BEATS = ('filebeat', 'metricbeat')


def test_list_modules(Command, beat):
    if beat.name in MODULES_BEATS:
        cmd = Command.run('%s modules list' % beat.name)

        assert cmd.rc == 0
        assert 'Enabled' in cmd.stdout
        assert 'Disabled' in cmd.stdout
        assert 'system' in cmd.stdout


def test_enable_module(Command, beat):
    if beat.name in MODULES_BEATS:
        cmd = Command.run('%s modules enable nginx' % beat.name)

        assert cmd.rc == 0
        assert cmd.stdout == 'Enabled nginx\n'
