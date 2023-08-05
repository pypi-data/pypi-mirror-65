String = str
DateTimeOffset = str
Uri = str
import datetime
import pytz

def getattrIgnoreCase(obj, attr, default=None):
    for i in dir(obj):
        if i.lower() == attr.lower():
            return getattr(obj, attr, default)
    return default


dtype_converter = {
    'int': 'int64',
    'bigint': 'int64',
    'long': 'int64',
    'float':'decimal',
    'double': 'double',
    'decimal.Decimal': 'decimal',
    'string': 'string',
    'bool': 'boolean',
    'datetime': 'dateTime',
    'timestamp': 'dateTime'
}


def to_utc_timestamp(d, format, tz=None):  
    if d is None or d == '':
        return ''  
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime.strptime(d, format)
    if tz:
        tz = pytz.timezone(tz)
        utc_time = tz.normalize(tz.localize(d)).astimezone(pytz.utc)
    else:
        utc_time = d.astimezone(pytz.utc)
    return str(int(utc_time.timestamp()))


def from_utc_timestamp(d, format, tz=None, offset_hour=False):
    if d is None or d == '' or d != d:
        return ''  
    d = str(d)
    if not offset_hour:
        tz = pytz.timezone(tz)
        utc_time = datetime.datetime.utcfromtimestamp(int(d.split(".")[0]))
        converted_time = tz.normalize(pytz.utc.localize(utc_time)).astimezone(tz)
    else:
        offset_hour = tz
        hour, minutes = map(int, offset_hour.split(":"))
        if hour < 0:
            days = -1
            total_second = 86400 - (((hour - 2*hour) * 60 + minutes) * 60)
        else:
            days = 0
            total_second = (hour * 60 + minutes) * 60
        converted_time = datetime.datetime.fromtimestamp(int(d.split(".")[0]), 
                            datetime.timezone(datetime.timedelta(days=days, seconds=total_second)))
    return converted_time.strftime(format)