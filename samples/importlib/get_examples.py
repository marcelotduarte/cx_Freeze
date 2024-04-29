from pathlib import Path
from urllib.request import urlopen

GITHUBUSERCONTENT = "https://raw.githubusercontent.com"

examples = [
    f"{GITHUBUSERCONTENT}/aio-libs/aiohttp/master/examples/server_simple.py",
    f"{GITHUBUSERCONTENT}/aio-libs/aiohttp/master/examples/web_srv.py",
    f"{GITHUBUSERCONTENT}/gevent/gevent/master/examples/wsgiserver.py",
]

for example in examples:
    filename = Path(example.split("/")[-1])
    with urlopen(example) as source:  # noqa: S310
        filename.write_bytes(source.read())
        print("Wrote", filename)
