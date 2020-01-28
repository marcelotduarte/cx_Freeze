from urllib.request import urlopen

examples = [
        'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/server_simple.py',
        'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/web_srv.py',
        'https://raw.githubusercontent.com/gevent/gevent/master/examples/wsgiserver.py'
]

for example in examples:
    fileName = example.split('/')[-1]
    with urlopen(example) as source, open(fileName, 'w+b') as target:
        target.write(source.read())
        print("Wrote", fileName)
