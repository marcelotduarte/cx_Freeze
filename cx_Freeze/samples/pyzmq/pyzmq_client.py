import time
import sys
import zmq
from contextlib import AbstractContextManager


class ignore(AbstractContextManager):
    def __init__(self, call):
        self.call = call

    def __enter__(self):
        if hasattr(self.call, "__enter__"):
            return self.call
        return self

    def __exit__(self, *exc_info):
        if hasattr(self.call, "__exit__"):
            return self.call.__exit__
        return None


port = 5556
timeout = None
for arg in sys.argv[1:]:
    if arg.startswith("--timeout="):
        timeout = int(arg[len("--timeout=") :])
    if arg.startswith("--port="):
        timeout = int(arg[len("--port=") :])
    elif arg.isdecimal():
        port = int(arg)

url = f"tcp://localhost:{port}"
request = "Ping"

context = zmq.Context()
socket = context.socket(zmq.REQ)

if timeout:
    timeout += time.monotonic()


print(f"Client connecting to {url}")
try:
    with ignore(socket.connect(url)):
        while True:
            if timeout and time.monotonic() >= timeout:
                request = "Close"
            print(f"Client sending: {request}")
            socket.send_string(request)
            reply = socket.recv_string()
            print(f"Client received: {reply}")
            if request == "Close":
                break
except KeyboardInterrupt:
    sys.exit(0)
