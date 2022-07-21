"""
Sample to show the datetime in RFC1123 (timezone is required)

zoneinfo version (new library in python 3.9)
"""

from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

RFC1123 = "%a, %d %b %Y %H:%M:%S %z"

utc_time = datetime.now(timezone.utc)
print("UTC time:", utc_time.strftime(RFC1123))

tz1 = ZoneInfo("America/Sao_Paulo")
brz_time = utc_time.astimezone(tz1)
print("Brazil time:", brz_time.strftime(RFC1123))

tz2 = ZoneInfo("US/Eastern")
eas_time = utc_time.astimezone(tz2)
print("US Eastern time:", eas_time.strftime(RFC1123))
