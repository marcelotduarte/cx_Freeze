"""Tests for hooks of zmq (pyzmq)."""

from __future__ import annotations

import threading

import pytest

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.venv
@zip_packages
def test_pyzmq(tmp_package, zip_packages: bool) -> None:
    """Test if pyzmq hook is working correctly."""
    tmp_package.create_from_sample("pyzmq")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    pyzmq_server = tmp_package.executable("pyzmq_server")
    assert pyzmq_server.is_file()
    pyzmq_client = tmp_package.executable("pyzmq_client")
    assert pyzmq_client.is_file()

    def thread_run(cmd: str, lines: list[str]) -> None:
        result = tmp_package.run(cmd)
        lines += result.outlines

    port = 5556 if zip_packages else 5555
    lines_server = []
    cmd_server = f"{pyzmq_server} {port}"
    thread_server = threading.Thread(
        target=thread_run, args=(cmd_server, lines_server)
    )

    lines_client = []
    cmd_client = f"{pyzmq_client} --port={port} --timeout=4"
    thread_client = threading.Thread(
        target=thread_run, args=(cmd_client, lines_client)
    )

    thread_server.start()
    thread_client.start()
    thread_server.join(TIMEOUT)
    thread_client.join(TIMEOUT)

    assert lines_server[0].startswith("Server listening at")
    assert lines_server[-1].endswith("Closing")
    assert lines_client[0].startswith("Client connecting to")
    assert lines_client[-1].endswith("Closing")
