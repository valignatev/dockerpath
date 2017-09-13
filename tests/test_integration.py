import os

import docker
import pytest


@pytest.fixture(scope='module')
def container():
    client = docker.from_env()
    print('building image')
    client.images.build(
        path=os.path.dirname(__file__),
        tag='dockerpath_test',
        rm=True,
    )
    print('creating and running container')
    # Need long-running command in order to keep container running
    container = client.containers.run(
        'dockerpath_test:latest',
        detach=True,
        name='dockerpath_test_cnt',
        command='top',
    )
    yield container
    print('stopping container')
    container.stop()
    print('removing container')
    container.remove()


@pytest.mark.xfail(reason='Not ready yet', raises=ImportError, strict=True)
def test_integration(container):
    import django
