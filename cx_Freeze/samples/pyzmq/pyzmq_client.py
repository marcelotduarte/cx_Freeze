import sys
import zmq

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5556

url = f"tcp://localhost:{port}"
request = "Ping"

context = zmq.Context()
socket = context.socket(zmq.REQ)

try:
    print(f"Client connecting to {url}")
    with socket.connect(url):
        while True:
            print(f"Client sending: {request}")
            socket.send_string(request)
            reply = socket.recv_string()
            print(f"Client received: {reply}")
except KeyboardInterrupt:
    sys.exit(0)
