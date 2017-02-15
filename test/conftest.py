from subprocess import run


def pytest_configure(config):
    run(['docker-compose', 'down'])
    run(['docker-compose', 'up', '--force-recreate', '-d'])


def pytest_unconfigure(config):
    run(['docker-compose', 'down'])
