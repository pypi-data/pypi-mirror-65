#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bigml_chronos import formats, util
from datetime import datetime, timedelta
from functools import partial
from isoweek import Week
import pytz
import re

def _formatter_basic(date_format, date):
    return util.custom_strptime(date, date_format)

def _formatter_basic_iso_date(date):
    return util.custom_strptime(date, "%Y%m%d%z")

def _formatter_basic_week_date(weekdate):
    iso_year,iso_week,iso_day = \
        util.try_read(weekdate, util.read_week_date)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day)

def _formatter_basic_week_date_time(date):
    iso_year, iso_week, iso_day, time = \
         util.try_read(date, util.read_week_date_time, msecs=True)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day) + time

def _formatter_basic_week_date_time_no_ms(date):
    iso_year, iso_week, iso_day, time = \
        util.try_read(date, util.read_week_date_time, msecs=False)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day) + time

def _formatter_iso_date(date):
    return util.custom_strptime(date, "%Y-%m-%d%z")

def _formatter_iso_date_time(date):
    return util.custom_strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

def _formatter_iso_instant(date):
    return util.custom_strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

def _formatter_iso_local_date(date):
    return util.custom_strptime(date, "%Y-%m-%d")

def _formatter_iso_local_date_time(date):
    return util.custom_strptime(date, "%Y-%m-%dT%H:%M:%S.%f")

def _formatter_iso_local_time(date):
    return util.custom_strptime(date, "%H:%M:%S.%f")

def _formatter_iso_offset_date(date):
    return util.custom_strptime(date, "%Y-%m-%d%z")

def _formatter_iso_offset_date_time(date):
    return util.custom_strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

def _formatter_iso_offset_time(date):
    return util.custom_strptime(date, "%H:%M:%S.%f%z")

def _formatter_iso_ordinal_date(date):
    year = date[:4]
    day = int(date.split("-")[1][:3])
    tz = date.split("-")[1][3:]
    return util.custom_strptime(year+tz, "%Y%z") + timedelta(days=day-1)

def _formatter_iso_time(date):
    return util.custom_strptime(date, "%H:%M:%S.%f%z")

def _formatter_iso_week_date(weekdate):
    iso_year,iso_week,iso_day, timezone = \
        util.try_read(weekdate, util.read_iso_week_date, tz=True)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day)

def _formatter_iso_zoned_date_time(date):
    return _formatter_iso_date_time(date)

def _formatter_rfc_1123_date_time(date):
    return util.custom_strptime(date, "%a, %d %b %Y %H:%M:%S GMT")

def _formatter_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp), tz=pytz.utc)

def _formatter_timestamp_msecs(timestamp):
    return datetime.fromtimestamp(float(timestamp)/1000, tz=pytz.utc)

def _formatter_odata_format(date):
    return _formatter_timestamp_msecs(date[6:-2])

def _formatter_week_date(weekdate):
    iso_year,iso_week,iso_day, timezone = \
        util.try_read(weekdate, util.read_iso_week_date, tz=False)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day)

def _formatter_week_date_time(date):
    iso_year, iso_week, iso_day, time = \
        util.try_read(date, util.read_hypen_week_date_time, msecs=True)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day) + time

def _formatter_week_date_time_no_ms(date):
    iso_year, iso_week, iso_day, time = \
        util.try_read(date, util.read_hypen_week_date_time, msecs=False)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day) + time

def _formatter_weekyear_week(weekdate):
    iso_year,iso_week = \
        util.try_read(weekdate, util.read_iso_week_date_no_day)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week)

def _formatter_weekyear_week_day(weekdate):
    iso_year,iso_week, iso_day, tz = \
        util.read_iso_week_date(weekdate, tz=False)
    week = Week(iso_year,iso_week)
    return util.date_from_week(week, iso_day)


custom_formatters = {"basic-iso-date": _formatter_basic_iso_date,
                     "basic-week-date": _formatter_basic_week_date,
                     "basic-week-date-time": _formatter_basic_week_date_time,
                     "basic-week-date-time-no-ms":
                     _formatter_basic_week_date_time_no_ms,
                     "iso-date": _formatter_iso_date,
                     "iso-date-time": _formatter_iso_date_time,
                     "iso-instant": _formatter_iso_instant,
                     "iso-local-date": _formatter_iso_local_date,
                     "iso-local-date-time": _formatter_iso_local_date_time,
                     "iso-local-time": _formatter_iso_local_time,
                     "iso-offset-date": _formatter_iso_offset_date,
                     "iso-offset-date-time": _formatter_iso_offset_date_time,
                     "iso-offset-time": _formatter_iso_offset_time,
                     "iso-ordinal-date": _formatter_iso_ordinal_date,
                     "iso-time": _formatter_iso_time,
                     "iso-week-date": _formatter_iso_week_date,
                     "iso-zoned-date-time": _formatter_iso_zoned_date_time,
                     "odata-format": _formatter_odata_format,
                     "rfc-1123-date-time": _formatter_rfc_1123_date_time,
                     "timestamp": _formatter_timestamp,
                     "timestamp-msecs": _formatter_timestamp_msecs,
                     "week-date": _formatter_week_date,
                     "week-date-time": _formatter_week_date_time,
                     "week-date-time-no-ms": _formatter_week_date_time_no_ms,
                     "weekyear-week": _formatter_weekyear_week,
                     "weekyear-week-day": _formatter_weekyear_week_day}

joda_to_python = {
    "Y": "%Y",
    "w": "%U",
    "e": "%w",
    "E": "%A",
    "y": "%y",
    "D": "%j",
    "M": "%m",
    "d": "%d",
    "a": "%p",
    "h": "%I",
    "H": "%H",
    "m": "%M",
    "s": "%S",
    "z": "%Z",
    "EEEE": "%A",
    "EE": "%a",
    "MMMM": "%B",
    "MMM": "%b",
    "YYYY": "%Y",
    "YY": "%y"}


def _accepted_joda_format(fmt):
    """Checks whether the format can be interpreted as a joda string and
    translated to Python

    """
    if re.sub("[^a-zA-Z]", "", re.sub("[%s]" % "".join(joda_to_python.keys()),
                                      "", fmt)) != "":
        raise ValueError("The %s datetime format cannot be handled in"
                         " local predictions." % fmt)
    return True


def _joda_to_python(fmt):
    """Translate a joda custom format to Python standards

    """
    keys = joda_to_python.keys()
    datetime_components = []
    last_char = ""
    word = ""
    for char in fmt:
        if char in keys:
            if last_char != char:
                if word != "":
                    datetime_components.append(word)
                    word = ""
            word +=char
        else:
            if word != "":
                datetime_components.append(word)
            datetime_components.append(char)
            word = ""

        last_char = char
    if word != "":
        datetime_components.append(word)

    for index in range(len(datetime_components)):
        word = datetime_components[index]
        if word in joda_to_python:
            datetime_components[index] = joda_to_python[word]
        elif word[0] in joda_to_python:
            datetime_components[index] = joda_to_python[word[0]]
    return "".join(datetime_components)


def _is_valid_format(fmt):
    return fmt in formats.dateformats.keys() or \
        fmt in formats.joda_strings.keys() or \
        _accepted_joda_format(fmt)


def _is_custom_format(fmt):
    return fmt == "[custom]"


def _get_formatter(format_name):
    if _is_valid_format(format_name):
        format_name = formats.joda_strings.get(format_name, format_name)
        dateformat = formats.dateformats.get(format_name, format_name)
        if _is_custom_format(dateformat):
            return custom_formatters.get(format_name)
        elif format_name not in formats.dateformats and \
                format_name not in formats.joda_strings:
            dateformat = _joda_to_python(format_name)
        return partial(_formatter_basic, dateformat)
    else:
        raise ValueError("Timeformat specified is not valid")


def _fix_time_format(date):
    pattern = re.search(r"((\+)[0-9][0-9](?!([0-9]|\:)))", date)
    if (pattern):
        timezone = pattern.groups()[0]
        date = date.replace(timezone, timezone + "00")
    return date


def _parse_with_format(format_name, date):
    '''Creates a datetime object from a string representing a date
    and its format

    :param string format_name: format name can represent the name of
    a date format (as "twitter-time") or the Joda directives
    used to parse it (as "YY-MM-dd"). Chronos will transform them into
    strptime directives
    :param string date: A string representing a datetime
    :raises: :class:`ValueError`: format_name not valid
    :raises: :class:`ValueError`: the date can't be parsed with format_name
    :returns: A Python date object
    :rtype: datetime
    '''
    # If the timezone is specified with only two digits (e.g. +00),
    # we have to add two additional zeros to it to be able to parse it
    # This can't be done with strptime directives
    formatter = _get_formatter(format_name)
    return formatter(_fix_time_format(date))


def _try_parse_with_format(format_name, date):
    ''' Same as _parse_with_format but returns None if the parsing fails'''
    output_date = None
    try:
        output_date = _parse_with_format(format_name, date)
    except (ValueError, IndexError) as e:
        pass
    return output_date


def _parse_with_formats(format_names, date):
    '''Creates a datetime object from a string representing a date
    and a list of its possible formats

    :param string format_names: List of the possible date
    formats. Each format name can represent the name of a date format
    (as "twitter-time") or the Joda directives used to parse it
    (as "YY-MM-dd"). Chronos will transform them into
    strptime directives
    :param string date: A string representing a datetime
    :raises: :class:`ValueError`: the date can't be parsed with any format
    :returns: A Python date object
    :rtype: datetime
    '''
    dates = map((lambda f: _try_parse_with_format(f, date)), format_names)
    possible_dates = [d for d in dates if d is not None]
    if len(possible_dates) == 0:
        raise ValueError("Cannot find a format for the specified date")
    else:
        return possible_dates[0]


def find_format(date):
    '''Finds the format name of a string representing a date.
    This format can be passed to the function parse_with_format
    to parse the date.

    :param string date: A string representing a datetime
    :raises: :class:`ValueError`: Cannot find a format
    :returns: The format of the date
    :rtype: string
    '''
    result = [[_try_parse_with_format(fmt, date), fmt]
              for fmt in formats.dateformats]
    filtered_result = [item for item in result if item[0] is not None]
    if(len(filtered_result) == 0):
        raise ValueError("Cannot find a format for the specified date")
    return filtered_result[0][1]


def parse(date, format_name=None, format_names=None):
    '''Creates a datetime object from a string representing a date and a
    format name, a list of possible format names or trying all the
    possible formats until it finds the correct one. If both
    format_name and format_names are passed, it will try all the
    possible formats in format_names and format_name.

    :param string date: A string representing a datetime
    :param string format_name: The  name of the date format, optional
    :param string format_names: A list with the possible date format names, optional
    :raises: :class:`ValueError`: Cannot find a format for the date
    :raises: :class:`ValueError`: the date can't be parsed with specified formats
    :returns: A Python date object
    :rtype: datetime

    '''
    if (format_name is None and format_names is None):
        date_format = find_format(date)
        output_date = _parse_with_format(date_format, date)
    elif (format_name is None and format_names is not None):
        output_date = _parse_with_formats(format_names, date)
    elif (format_name is not None and format_names is None):
        output_date = _parse_with_format(format_name, date)
    else:
        format_names.append(format_name)
        output_date = _parse_with_formats(format_names, date)
    return output_date
