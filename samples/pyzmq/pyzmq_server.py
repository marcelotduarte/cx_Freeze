from __future__ import annotations

import sys
import time
from contextlib import AbstractContextManager

import zmq


class ignore(AbstractContextManager):
    def __init__(self, call) -> None:
        self.call = call

    def __enter__(self):  # noqa: ANN204
        if hasattr(self.call, "__enter__"):
            return self.call
        return self

    def __exit__(self, *exc_info):  # noqa: ANN204
        if hasattr(self.call, "__exit__"):
            return self.call.__exit__
        return None


port = int(sys.argv[1]) if len(sys.argv) > 1 else 5556

url = f"tcp://*:{port}"
reply = "Pong"

context = zmq.Context()
socket = context.socket(zmq.REP)

print(f"Server listening at {url}")
try:
    with ignore(socket.bind(url)):
        while True:
            message = socket.recv_string()
            print(f"Server received: {message}")
            if message == "Close":
                reply = "Closing"
            else:
                time.sleep(1)
            print(f"Server sending: {reply}")
            socket.send_string(reply)
            if message == "Close":
                break
except KeyboardInterrupt:
    sys.exit(0)
