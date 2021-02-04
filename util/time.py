from timezonefinder import TimezoneFinder
import pytz
import datetime


def timezone_name_from_coordinates(lng: float, lat: float) -> str:
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lng, lat=lat)


def utcoffset_from_timezone_name(name: str) -> int:
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone(name))

    pst_utcoffset = pst_now.utcoffset()
    pst_utcoffset_hours = pst_utcoffset.seconds / 60 / 60
    utcoffset = pst_utcoffset_hours if pst_utcoffset.days >= 0 else -(24 - pst_utcoffset_hours)

    return int(utcoffset)
