'''sample to show the datetime in RFC1123 (timezone is required)'''
from datetime import datetime
import pytz
import tzlocal

RFC1123 = '%a, %d %b %Y %H:%M:%S %z'

try:
    tz = tzlocal.get_localzone()
    print('Using your local timezone:', tz.zone)
except pytz.exceptions.UnknownTimeZoneError as exc:
    print('Detected your local timezone:', exc.args[0])
    print("WARNING: fail to load pytz timezones, fallback to UTC")
    tz = pytz.utc
finally:
    print(datetime.now(tz).strftime(RFC1123))
