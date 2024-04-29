"""Sample to show the datetime in RFC1123 (timezone is required).

pytz version
"""

from __future__ import annotations

import datetime

import pytz

RFC1123 = "%a, %d %b %Y %H:%M:%S %z"

utc_time = datetime.datetime.now(pytz.utc)
print("UTC time:", utc_time.strftime(RFC1123))

tz1 = pytz.timezone("America/Sao_Paulo")
brz_time = utc_time.astimezone(tz1)
print("Brazil time:", brz_time.strftime(RFC1123))

tz2 = pytz.timezone("US/Eastern")
eas_time = utc_time.astimezone(tz2)
print("US Eastern time:", eas_time.strftime(RFC1123))
