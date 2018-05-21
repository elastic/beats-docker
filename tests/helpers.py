import subprocess
import os


def run(beat, command):

    caps = ''
    if beat.name == 'packetbeat':
        caps = '--cap-add net_admin --cap-add net_raw'

    if beat.name == 'heartbeat':
        caps = '--cap-add net_raw'

    if beat.name == 'auditbeat':
        caps = '--cap-add audit_control --pid=host'

    cli = 'docker run %s --rm --interactive %s %s' % (caps, beat.image, command)
    result = subprocess.run(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.stdout = result.stdout.rstrip()
    return result
