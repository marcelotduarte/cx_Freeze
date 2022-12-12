from __future__ import annotations

import orjson

print(orjson.dumps({"a": "b", "c": {"d": True}, "e": [1, 2]}))
print(
    orjson.dumps(
        {"a": "b", "c": {"d": True}, "e": [1, 2]}, option=orjson.OPT_INDENT_2
    ).decode()
)
