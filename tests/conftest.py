from subprocess import run


def pytest_configure(config):
    beats = open('beats.txt').read().strip().split("\n")
    run(['docker-compose', 'down'])
    run(['docker-compose', 'up', '--force-recreate', '-d', '--no-deps'] + beats)


def pytest_unconfigure(config):
    run(['docker-compose', 'down'])
