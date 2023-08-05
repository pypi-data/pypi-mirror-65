import calendar
import datetime

import pytz

from medallion.common import datetime_to_float, string_to_datetime

if __name__ == '__main__':
    timestamp_str = "2019-11-24T23:29:07.434659Z"

    epoch_naive = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
    epoch_utc = epoch_naive.replace(tzinfo=pytz.UTC)

    dt_naive = string_to_datetime(timestamp_str)
    dt_utc = dt_naive.replace(tzinfo=pytz.UTC)

    diff_naive = (dt_naive - epoch_naive).total_seconds()
    diff_utc = (dt_utc - epoch_utc).total_seconds()
    diff_medallion = datetime_to_float(dt_naive)
    diff_calendar = calendar.timegm(dt_naive.utctimetuple())

    print("Naive epoch difference:\t", diff_naive)
    print("UTC epoch difference:\t", diff_utc)
    print("Medallion difference:\t", diff_medallion)
    print("Via calendar.timegm():\t", diff_calendar)
