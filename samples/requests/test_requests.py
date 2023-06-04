from __future__ import annotations

import requests

print("Hello from cx_Freeze")
try:
    r = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    print(r.json())
except requests.exceptions.RequestException as exc:
    print(exc)
