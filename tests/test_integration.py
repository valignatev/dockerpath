import os
import sys

import docker
import pytest

import dockerpath


TEST_CONTAINER_NAME = 'dockerpath_test_cnt'


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
        name=TEST_CONTAINER_NAME,
        command='top',
    )
    yield container
    print('stopping container')
    container.stop()
    print('removing container')
    container.remove()


def test_can_not_import_if_was_not_setup(container):
    with pytest.raises(ImportError):
        import django


@pytest.mark.xfail(reason='Not ready yet', raises=AssertionError, strict=True)
def test_modifies_sys_path_on_setup():
    old_sys_path = sys.path.copy()
    dockerpath.setup('dockerpaht_test_cnt')
    new_sys_path = sys.path.copy()
    assert len(new_sys_path) > len(old_sys_path)


@pytest.mark.xfail(reason='Not ready yet', raises=ImportError, strict=True)
def test_successfully_imports_if_setup(container):
    dockerpath.setup(TEST_CONTAINER_NAME)
    import django
