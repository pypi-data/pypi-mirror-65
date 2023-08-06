import time
import dateutil.tz
from datetime import datetime


def current_time_int():
    return int(time.time())


def current_time_string(string_format="%Y-%m-%d %H:%M:%S %Z"):
    utc_now = datetime.now(tz=dateutil.tz.UTC)
    return utc_now.strftime(string_format)
