from dockerpath import parse_remote_path, with_container_info


# cmd is 'python -c "import sys\nfor path in sys.path:print(path)"'
raw_output = b'\n/usr/local/lib/python36.zip\n/usr/local/lib/python3.6\n/usr/local/lib/python3.6/lib-dynload\n/usr/local/lib/python3.6/site-packages\n'  # noqa


def test_parses_remote_path():
    remote_path = parse_remote_path(raw_output)
    assert remote_path == [
        '',
        '/usr/local/lib/python36.zip',
        '/usr/local/lib/python3.6',
        '/usr/local/lib/python3.6/lib-dynload',
        '/usr/local/lib/python3.6/site-packages',
    ]


def test_prepends_remote_paths_with_container_info():
    modified_remote_path = with_container_info(
        'cnt_name',
        parse_remote_path(raw_output),
    )
    assert modified_remote_path == [
        'cnt_name:',
        'cnt_name:/usr/local/lib/python36.zip',
        'cnt_name:/usr/local/lib/python3.6',
        'cnt_name:/usr/local/lib/python3.6/lib-dynload',
        'cnt_name:/usr/local/lib/python3.6/site-packages',
    ]
