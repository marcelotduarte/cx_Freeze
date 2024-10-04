"""Sample to show the datetime in RFC1123 (timezone is required)."""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import TZPATH, ZoneInfo, available_timezones

RFC1123 = "%a, %d %b %Y %H:%M:%S %z"

print("TZPATH:", TZPATH)
print("Available timezones:", len(available_timezones()))

utc_time = datetime.now(timezone.utc)
print("UTC time:", utc_time.strftime(RFC1123))

tz1 = ZoneInfo("America/Sao_Paulo")
brz_time = utc_time.astimezone(tz1)
print("Brazil time:", brz_time.strftime(RFC1123))

tz2 = ZoneInfo("US/Eastern")
eas_time = utc_time.astimezone(tz2)
print("US Eastern time:", eas_time.strftime(RFC1123))
