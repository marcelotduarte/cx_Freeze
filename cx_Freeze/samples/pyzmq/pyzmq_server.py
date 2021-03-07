import time
import sys
import zmq

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5556

url = f"tcp://*:{port}"
reply = "Pong"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(url)


try:
    print(f"Server listening at {url}")
    while True:
        message = socket.recv_string()
        print(f"Server received: {message}")
        time.sleep(1)
        print(f"Server sending: {reply}")
        socket.send_string(reply)
except KeyboardInterrupt:
    sys.exit(0)
