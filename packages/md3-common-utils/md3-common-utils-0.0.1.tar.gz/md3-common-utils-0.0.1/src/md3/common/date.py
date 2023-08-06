import re
import datetime
import calendar


def add_months(dt, months):
    """
    Add months to the dt datetime
    """
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day, dt.hour, dt.minute, dt.second)


def sub_months(dt, months):
    """
    subtract months to the dt datetime
    """
    year = dt.year
    month = dt.month - months
    while month < 1:
        year -= 1
        month += 12
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day, dt.hour, dt.minute, dt.second)


def diff_month(d1, d2):
    """
    Helper function to calculate the number of month between two dates
    @param d1:
    @param d2:
    @return:
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def convert_datetime_formats(datetime_str, from_format, to_format):
    """
    Convert one given date string in a specific format to a new format.
    If original format does not match the date string, the string is returned unchanged.

    :param datetime_str: A string representing a date / datetime
    :param from_format: The format the given string is in
    :param to_format: the wanted format
    :return: the given date in the the new format (or unchanged if original format was not matched)
    """
    try:
        datetime_obj = datetime.datetime.strptime(datetime_str, from_format)
        return datetime_obj.strftime(to_format)
    except ValueError as error:
        return datetime_str


def reformat_datetime(orig_date, new_format):
    """
    Receive a string date YYYY-MM-DD[T| ][HH:MM[:SS]] and return in the requested format

    :param orig_date: A string representing a datetime in format YYYY-MM-DD[T| ][HH:MM[:SS]]
    :param new_format: New format wanted (datetime.strftime formats allowed)
    """
    datetime_obj = generic_strptime(orig_date)
    return datetime_obj.strftime(new_format) if datetime_obj is not None else orig_date


def generic_strptime(datetime_str):
    """
    Receive a string date YYYY-MM-DD[T| ][HH:MM[:SS]] and return timestamp object or None
    :param datetime_str: A string representing a datetime in format YYYY-MM-DD[T| ][HH:MM[:SS]]
    :return: timestamp object or None
    """
    result = None

    if datetime_str is not None:
        m = re.match(r"^(\d\d\d\d)\-(\d+)\-(\d+)[T ]?((\d+):(\d+))?(:(\d+))?", datetime_str)
        if m:
            g = m.groups()
            result = datetime.datetime(
                year=int(g[0]), month=int(g[1]), day=int(g[2]),
                hour=int(g[4]), minute=int(g[5]), second=int(g[7])
            )

    return result
