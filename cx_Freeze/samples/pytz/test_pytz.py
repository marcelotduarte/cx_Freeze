'''sample to show the datetime in RFC1123 (timezone is required)'''
import datetime
import pytz

RFC1123 = '%a, %d %b %Y %H:%M:%S %z'

utc_time = datetime.datetime.utcnow()
print('UTC time:', utc_time.strftime(RFC1123))

tz1 = pytz.timezone('America/Sao_Paulo')
brz_time = tz1.fromutc(utc_time)
print('Brazil time:', brz_time.strftime(RFC1123))

tz2 = pytz.timezone('US/Eastern')
eas_time = tz2.fromutc(utc_time)
print('US Eastern time:', eas_time.strftime(RFC1123))
