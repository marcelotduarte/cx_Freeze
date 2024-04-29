"""WSGI server example."""

from __future__ import annotations

from gevent.pywsgi import WSGIServer


def application(env, start_response) -> list[bytes]:
    if env["PATH_INFO"] == "/":
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"<b>hello world</b>"]

    start_response("404 Not Found", [("Content-Type", "text/html")])
    return [b"<h1>Not Found</h1>"]


if __name__ == "__main__":
    print("Serving on 8088...")
    WSGIServer(("127.0.0.1", 8088), application).serve_forever()
