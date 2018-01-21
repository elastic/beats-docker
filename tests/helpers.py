import subprocess
import os


def run(beat, command):
    image = 'docker.elastic.co/beats/%s:%s' % (beat.name, beat.tag)

    caps = ''
    if beat.name == 'packetbeat':
        caps = '--cap-add net_admin --cap-add net_raw'

    if beat.name == 'heartbeat':
        caps = '--cap-add net_raw'

    if beat.name == 'auditbeat':
        caps = '--cap-add audit_control --pid=host'

    cli = 'docker run %s --rm --interactive %s %s' % (caps, image, command)
    result = subprocess.run(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result.stdout = result.stdout.rstrip()
    return result
