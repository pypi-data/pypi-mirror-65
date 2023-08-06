import json
import re
from collections import OrderedDict
from datetime import datetime, timedelta


'''
PARSERS
_______________________
'''


def absolute_date(str_date):
    ''' finds a date in a iso-type format 
    input : str() : "2020-01-20" or "2020-01-20T12" or "2020-01-20T17:44:34.581634Z"
    output : {"found":True|False, "datetime":datetime()}

    '''
    if type(str_date) != str:
        return{"found": False}
    match = re.search(
        '([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])T?([0-2][0-9])?:?([0-5][0-9])?:?([0-5][0-9])?.?([0-9]{6})?', str_date)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hours = int(match.group(4) if match.group(4) is not None else 0)
        minutes = int(match.group(5) if match.group(5) is not None else 0)
        seconds = int(match.group(6) if match.group(6) is not None else 0)
        milli = int(match.group(7) if match.group(7) is not None else 0)
        return {"found": True, "datetime": datetime(year, month, day, hours, minutes, seconds, milli)}
    else:
        return {"found": False}


def relative_date(str_date):
    ''' finds a date in a relative format (relative to datetime.now)
    input : str() : "days:1", "days:4", "hours:10", "minutes:10"
    output : {"found":True|False, "datetime":datetime()}

    '''
    try:
        str_splitted = str_date.split(':')
        if str_splitted[0] == "minutes":
            return {"found": True, "datetime": datetime.utcnow() + timedelta(minutes=int(str_splitted[1]))}
        elif str_splitted[0] == "hours":
            return {"found": True, "datetime": datetime.utcnow() + timedelta(hours=int(str_splitted[1]))}
        elif str_splitted[0] == "days":
            return {"found": True, "datetime": datetime.utcnow() + timedelta(days=int(str_splitted[1]))}
        return {"found": False}
    except:
        return {"found": False}


def get_abs_rel_date(str_date):
    ''' Combines absolute_date and relative_date
    input: str() (see above)
    output:datetime()|None
    '''
    absolute = absolute_date(str_date)
    if absolute["found"]:
        return absolute["datetime"]
    relative = relative_date(str_date)
    if relative["found"]:
        return relative["datetime"]
    else:
        return str_date


def str_to_timedelta(str_date):
    try:
        str_splitted = str_date.split(":")
        if str_splitted[0] == "minutes":
            return timedelta(minutes=int(str_splitted[1]))
        elif str_splitted[0] == "hours":
            return timedelta(hours=int(str_splitted[1]))
        elif str_splitted[0] == "days":
            return timedelta(days=int(str_splitted[1]))
        return None
    except:
        return None


'''
TIMEFRAME
'''

mapping = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class TimeFrame():
    def __init__(self, timeframe):
        detailed_timeframe = {}
        for k, v in timeframe.items():
            days = k.split(':')
            start_day = mapping.index(days[0])
            end_day = start_day + \
                0 if len(days) == 1 else mapping.index(days[1])
            for d in range(start_day, end_day+1):
                hours_ranges = v.split("-")
                hours_detailed = []
                for hours_range in hours_ranges:
                    hours = hours_range.split(":")
                    if len(hours) == 2:
                        for h in range(int(hours[0]), int(hours[1])):
                            hours_detailed.append(h)
                detailed_timeframe[d] = sorted(hours_detailed)
        self.timeframe = sorted(detailed_timeframe.items(), key=lambda t: t[0])
        self.raw_timeframe = timeframe

    def is_in_timeframe(self, datetime_obj):
        if datetime_obj.weekday() in self.timeframe:
            if datetime_obj.hour in self.timeframe[datetime_obj.weekday()]:
                return True
        return False

    def get_closest(self, datetime_obj):
        return min(self.generate_datetimes(datetime_obj), key=lambda x: abs(x - datetime_obj))

    def get_next(self, datetime_obj):
        list_above = [i for i in self.generate_datetimes(
            datetime_obj) if i >= datetime_obj]
        return min(list_above, key=lambda x: abs(x - datetime_obj))

    def generate_datetimes(self, datetime_obj, before=2, after=2):
        list_timeframe = []
        long_timeframe = {}
        weekday = datetime_obj.weekday()
        for k, v in self.timeframe:
            long_timeframe[k-7] = v
            long_timeframe[k] = v
            long_timeframe[k+7] = v

        long_timeframe = OrderedDict(
            sorted(long_timeframe.items(), key=lambda t: t[0]))
        closest_day = min(long_timeframe, key=lambda x: abs(x-weekday))
        list_long_timeframe = list(long_timeframe.items())
        for weekday, hours in list_long_timeframe[list(long_timeframe.keys()).index(closest_day)-2:list(long_timeframe.keys()).index(closest_day)+2]:
            delta_weekday = weekday-datetime_obj.weekday()
            for h in hours:
                list_timeframe.append(datetime(
                    datetime_obj.year, datetime_obj.month, datetime_obj.day+delta_weekday, h, 0, 0, 0))

        return list_timeframe
