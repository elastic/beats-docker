from .fixtures import beat


def test_labels(beat):
    labels = beat.docker_metadata['Config']['Labels']
    assert labels['org.label-schema.name'] == beat.name
    assert labels['org.label-schema.schema-version'] == '1.0'
    assert labels['org.label-schema.url'] == 'https://www.elastic.co/products/beats/' + beat.name
    assert labels['org.label-schema.vcs-url'] == 'https://github.com/elastic/beats-docker'
    assert labels['org.label-schema.vendor'] == 'Elastic'
    assert labels['org.label-schema.version'] == beat.tag
    if beat.flavor == 'oss':
        assert labels['license'] == 'Apache-2.0'
    else:
        assert labels['license'] == 'Elastic License'
