import os
import sys

import docker
import pytest

import dockerpath


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


@pytest.fixture
def expected_raw_sys_path():
    return (
        b'\n'
        b'/usr/local/lib/python36.zip\n'
        b'/usr/local/lib/python3.6\n'
        b'/usr/local/lib/python3.6/lib-dynload\n'
        b'/usr/local/lib/python3.6/site-packages\n'
    )


def test_can_not_import_if_was_not_setup(container):
    with pytest.raises(ImportError):
        import django


def test_able_to_get_sys_path_from_container(container, expected_raw_sys_path):
    assert expected_raw_sys_path == dockerpath.remote_sys_path(container)


def test_modifies_sys_path_on_setup(container):
    old_sys_path = sys.path.copy()
    dockerpath.setup(container.name)
    new_sys_path = sys.path.copy()
    diff = set(new_sys_path) - set(old_sys_path)
    assert 5 == len(new_sys_path) - len(old_sys_path)
    for path in diff:
        assert '{}:'.format(container.name) in path


@pytest.mark.xfail(reason='Not ready yet', raises=ImportError, strict=True)
def test_successfully_imports_if_setup(container):
    dockerpath.setup(container.name)
    import django
