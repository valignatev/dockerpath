import sys

import docker


def setup(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    container_sys_path = with_container_info(
        container.name,
        parse_remote_path(
            remote_sys_path(container)
        )
    )
    sys.path += container_sys_path


def remote_sys_path(container):
    return container.exec_run(
        cmd='python -c "import sys\nfor path in sys.path:print(path)"'
    )


def parse_remote_path(raw_path: bytes) -> list:
    return raw_path.decode().split('\n')[:-1]


def with_container_info(container_name: str, path) -> list:
    return ['dockerpath-{}:{}'.format(container_name, p) for p in path]
