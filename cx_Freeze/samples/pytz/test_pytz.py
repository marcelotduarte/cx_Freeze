from datetime import datetime
from tzlocal import get_localzone

RFC1123 = '%a, %d %b %Y %H:%M:%S %z'

try:
    tz = get_localzone()
except:
    import pytz
    tz = pytz.utc
    print("WARNING: fail to load pytz timezones")
finally:
    print(datetime.now(tz).strftime(RFC1123))
