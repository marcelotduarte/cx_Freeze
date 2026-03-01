import os

import requests
from requests.utils import DEFAULT_CA_BUNDLE_PATH

print("Hello from cx_Freeze")
print(DEFAULT_CA_BUNDLE_PATH)
print(os.environ.get("SSL_CERT_FILE"))

try:
    r = requests.get(
        "https://jsonplaceholder.typicode.com/todos/1", timeout=10
    )
    print(r.json())
except requests.exceptions.RequestException as exc:
    print(exc)
