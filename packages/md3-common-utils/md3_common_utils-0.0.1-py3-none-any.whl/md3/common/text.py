import datetime
import math
import mimetypes
import re

import unidecode


def trim(text_input):
    """
    Function to remove the multiple space on string.

    :param text_input: input text to parse
    :return: text parsed
    """

    text_output = ' '.join([k for k in text_input.split(" ") if k])

    return text_output


def str2bool(value, null_boolean=False):
    """
    Helper function to convert a string into a correct
    boolean value.

    :param object value: should be a string
    :param boolean null_boolean: Accept null value
    :return: boolean
    """

    if isinstance(value, bool):
        return value

    if value in [None, "", "null"] and null_boolean:
        return None

    value_string = str(value)

    if value_string.lower() in ("oui", "yes", "on", "true", "t", "1"):
        return True
    elif value_string.lower() in ("non", "no", "off", "false", "f", "0", "-1"):
        return False

    return False


def str2datetime(value, formats=None):
    formats = formats if formats is not None else ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
    for f in formats:
        try:
            return datetime.datetime.strptime(value, f)
        except ValueError:
            continue


def convert_to_number(value, default=0, number_type=float, **kwargs):
    """
    Helper function to convert a alpha numeric string to a given
    number type (float or int).

    :param value:
    :param float default:
    :param number_type: Number type for the conversion float or int
    :return:
    """

    try:
        if isinstance(value, str):
            non_alpha = re.compile(r"[^\d.]+")
            replacement = kwargs.get("replacement", {})
            value = non_alpha.sub("", value.replace(replacement.get("what", ","), replacement.get("by", "")))

        if number_type.__name__ == "float":
            value = float(value)
        elif number_type.__name__ == "int":
            if kwargs.get("floor") is True:
                value = math.floor(float(value))
            elif kwargs.get("ceil") is True:
                value = math.ceil(float(value))
            else:
                value = int(float(value))
    except (AttributeError, ValueError, Exception):
        value = default

    return value


def csv_prepare_entry(value):
    """
    Converts a "None" value into an empty string
    :param value:
    :return: <""> if value is none, <value> otherwise
    """
    return "" if value is None else str(value).replace(";", ",")


def to_html(value, main_tag="p"):
    """
    If value is a string and not starting with an HTML tag:
     + Convert "\n" to <br/>
     + Place all content inside <main_tag> HTML tag

    :param value: string to process
    :param main_tag: HTML tag to apply around all content
    :return: processed value if is str, else: the original value unchanged
    """

    if isinstance(value, str):
        value = value.strip()
        start_tag = ""
        end_tag = ""

        if len(value) > 0 and value[0] != "<":
            if main_tag and main_tag != "":
                start_tag = "<%s>" % main_tag
                end_tag = "</%s>" % main_tag

            value = "%s%s%s" % (start_tag, value.replace("\r", "").replace("\n", "<br/>"), end_tag)

    return value


def reverse_date_strings(dict_obj, key_prefixes=(), key_suffixes=(), key_names=(), format_func=None):
    """
    Reverses dates found on a list or dict in international format (YYYY-MM-DD) to
    convert to french format (DD-MM-YYYY).

    :param dict_obj: Dictionary or list where to search strings (recursively)
    :param key_prefixes: List of prefixes of keys to process
    :param key_suffixes: List of sufixes of keys to process
    :param key_names: List of keys to process
    :param format_func: alternative function to format a date string
    :return: None, replacements are made inline!
    """

    if len(key_prefixes) == 0 and len(key_suffixes) == 0 and len(key_names) == 0:
        return

    if isinstance(key_prefixes, str):
        key_prefixes = [key_prefixes]

    if isinstance(key_suffixes, str):
        key_suffixes = [key_suffixes]

    if isinstance(key_names, str):
        key_names = [key_names]

    if isinstance(dict_obj, list):
        for item in dict_obj:
            reverse_date_strings(
                dict_obj=item,
                key_prefixes=key_prefixes,
                key_suffixes=key_suffixes,
                key_names=key_names,
                format_func=format_func
            )

    elif isinstance(dict_obj, dict):
        if format_func is None:
            def default_format_func(date_str):
                return "-".join(reversed(date_str[:10].split("-")))

            format_func = default_format_func

        for k, v in dict_obj.items():
            if isinstance(v, str):
                if k in key_names or \
                        len([1 for p in key_prefixes if k.startswith(p)]) > 0 or \
                        len([1 for s in key_suffixes if k.endswith(s)]) > 0:
                    dict_obj[k] = format_func(v)
            else:
                reverse_date_strings(
                    dict_obj=v,
                    key_prefixes=key_prefixes,
                    key_suffixes=key_suffixes,
                    key_names=key_names,
                    format_func=format_func
                )


def reverse_date_strings_with_time(date_str):
    """
    Function to use as a parameter for reverse_date_strings(format_func=reverse_date_strings_with_time)
    Reverses date and keeps HH:MM at the end if it exists on original string.

    :return: String formatted
    """

    date_parts = date_str.replace("T", " ")[:16].split(" ")
    date_parts[1] = " %s" % date_parts[1] if len(date_parts) > 1 else ""

    return "%s%s" % ("-".join(reversed(date_parts[0].split("-"))), date_parts[1])


def format_bytes(size):
    labels = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    n = 0
    while n < (len(labels) - 1) and size > 1024:
        size /= 1024
        n += 1

    return size, labels[n]


def get_nested_value(obj, path):
    """
    Explores obj recursively and returns the value found at path.
    Path separator is '.'
    Searches for keys, indexes and attributes at object

    :param obj: object to explore
    :param path: path to retrieve
    :return: value found at path or None if path is invalid
    """

    paths = path.split(".")
    path = paths.pop(0)

    # Get path as an attribute
    value = getattr(obj, path, None)

    # Get path as a dict key
    if value is None and getattr(obj, "get", False):
        value = obj.get(path)

    # Get path as a list index
    if value is None:
        try:
            value = obj[int(path)]
        except (ValueError, TypeError, IndexError):
            pass

    return value if len(paths) == 0 else get_nested_value(value, ".".join(paths))


def decimal_to_coordinate(decimal):
    result = str(decimal)
    if len(result) < 8 and result.startswith("-"):
        result = result[1:]
        while len(result) < 7:
            result = "0" + result
        result = "-0." + result
    elif len(result) < 7:
        while len(result) < 7:
            result = "0" + result
        result = "0." + result
    else:
        result = result[:-7] + "." + result[-7:]
    return float(result)


def strip_strings(obj):
    """
    Recursively strip all strings found on an object.

    :param obj: obj to process
    :return: object processed
    """

    result = obj

    if isinstance(obj, list):
        result = [strip_strings(obj[i]) for i in range(len(obj))]
    elif isinstance(obj, dict):
        result = {k: strip_strings(v) for k, v in obj.items()}
    elif isinstance(obj, str):
        result = obj.strip()

    return result


def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)


def convert_value_to_datetime(d):
    """
    Helper that converts all fields that might be a date in a dictionary
    to a datetime.

    :param d:
    :return:
    """

    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = convert_value_to_datetime(v)
        elif isinstance(v, list):
            x = list()
            # we need a better way to recursively do this for all the values
            for l in v:
                if isinstance(l, dict):
                    x.append(convert_value_to_datetime(l))
                else:
                    x.append(l)

            d[k] = x
        else:
            d[k] = v

            if not isinstance(v, bool) and ("date" in k or k == "created" or k == "updated" or k.endswith("_date")):
                try:
                    if isinstance(v, int):
                        # dummy way to check if it is in seconds or milliseconds
                        if v > 9999999999:
                            v = int(v / 1000)

                        d[k] = datetime.datetime.fromtimestamp(v)
                    else:
                        tokens = v.replace(" ", "T").split("T")

                        if len(tokens) == 1:
                            d[k] = datetime.datetime.strptime(v, "%Y-%m-%d")
                        elif len(tokens) == 2:
                            d[k] = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                except (ValueError, AttributeError, Exception):
                    pass

    return d


def convert_datetime_to_str(value, str_format="%Y-%m-%d"):
    """
    Helper that converts all fields that might be a date or datetime in a dictionary
    to a specific string format.

    :param value:
    :param str_format:
    :return:
    """

    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = convert_datetime_to_str(value=v, str_format=str_format)
        elif isinstance(v, list):
            x = list()
            # we need a better way to recursively do this for all the values
            for l in v:
                if isinstance(l, dict):
                    x.append(convert_datetime_to_str(value=l, str_format=str_format))
                else:
                    x.append(l)
            value[k] = x
        else:
            value[k] = v

            if not isinstance(v, bool) and ("date" in k or k == "created" or k == "updated"):
                try:
                    value[k] = v.strftime(str_format)
                except (ValueError, AttributeError, Exception):
                    pass

    return value


def guess_extention(mime_type):
    """returns an extention fot the given mime type"""
    ext = mime_type.split("/")[-1]
    if len(ext) > 4:
        ext = mimetypes.guess_extension(mime_type)[1:]

    if ext in ["jpe", "jpeg"]:
        ext = "jpg"

    return ext


def check_url(url):
    """
    Helper function to check if a url starts with http or https, if not
    corrects it with https:// in the start of the string.

    :param url:
    :return:
    """

    if url:
        for starts in ["http://", "https://", "front:", "/", "mailto:", "tel:", "sms:"]:
            if url.lower().startswith(starts):
                break
        else:
            url = "https://" + url
    else:
        url = ""

    return url


def break_line_html(text):
    """
    Helper function to convert text with \n to html with <br/>. This function are 
    used for example on the textarea to add message to be sent by email.
    
    @param text:
    @return: text with <br> instead of \n or \r\n
    """

    return text.replace("\r\n", "<br/>").replace("\n", "<br/>")
