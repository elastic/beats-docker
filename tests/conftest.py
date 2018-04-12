from subprocess import run


def get_compose_file(config):
    return 'docker-compose-%s.yml' % config.getoption('--image-flavor')


def pytest_addoption(parser):
    """Customize testinfra with config options via cli args"""
    # Let us specify which docker-compose-(image_flavor).yml file to use
    parser.addoption('--image-flavor', action='store',
                     help='Docker image flavor; the suffix used in docker-compose-<flavor>.yml')


def pytest_configure(config):
    run(['docker-compose', '-f', get_compose_file(config), 'down'])
    run(['docker-compose', '-f', get_compose_file(config), 'up', '--force-recreate', '-d', '--no-deps'])


def pytest_unconfigure(config):
    run(['docker-compose', '-f', get_compose_file(config), 'down'])
