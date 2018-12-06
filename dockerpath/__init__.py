import os
import sys
import tarfile
import tempfile

import docker


def setup(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    container_sys_path = parse_remote_path(remote_sys_path(container))
    remote_paths_to_prepend = []
    for path in filter(None, container_sys_path):
        remote_path_list = path.split('/')
        local_path = os.path.join(*(['.dockerpath', container.name] + remote_path_list[:-1]))
        with tempfile.NamedTemporaryFile() as tmp:
            try:
                data, _ = container.get_archive(path)
            except docker.errors.NotFound as e:
                print(e.explanation)
                continue
            else:
                for chunk in data.stream():
                    tmp.write(chunk)
            tmp.seek(0)
            with tarfile.open(mode='r', fileobj=tmp) as tar:
                tar.extractall(local_path)
        remote_paths_to_prepend.append(os.path.join(local_path, remote_path_list[-1]))
    sys.path = remote_paths_to_prepend + sys.path


def remote_sys_path(container):
    return container.exec_run(
        cmd='python -c "import sys\nfor path in sys.path:print(path)"'
    )


def parse_remote_path(raw_path: bytes) -> list:
    return raw_path.decode().split('\n')[:-1]


def with_container_info(container_name: str, path) -> list:
    return ['dockerpath-{}:{}'.format(container_name, p) for p in path]
