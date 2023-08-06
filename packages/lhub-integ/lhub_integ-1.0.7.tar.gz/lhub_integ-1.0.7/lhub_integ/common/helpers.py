import json
import random
import string
import sys
import netaddr
import datetime
import dateutil
import dateutil.tz

import jinja2
import time
from collections import OrderedDict

from lhub_integ.common.input_helpers import __get_stripped_env_float
from lhub_integ.common import constants as global_constants


# Please make sure that Errors are passed in function in below format only:
# [{'message': 'blah-blah', 'inputId': 'access_key'}, .... , {'message': 'blah-again', 'inputId': 'server_url'}]
# otherwise your error message won't be able to be parsed correctly.


def print_validation_message(error):
    print("[result] %s" % json.dumps(error), file=sys.stderr)
    sys.exit(1)


def exit_with_instantiation_errors(code, errors, message="Integration validation failed."):
    error_wrapper = {"errors": errors, "message": message}
    print("[result] %s" % json.dumps(error_wrapper), file=sys.stderr)
    sys.exit(code)


def exit_with_error_message(code, msg):
    error = {"errors": [], "message": msg}
    print("[result] %s" % json.dumps(error), file=sys.stderr)
    sys.exit(code)


# Use this method when you do not care for fields from parent table
def print_result(result):
    if isinstance(result, dict):
        result = json.dumps(result)
    print("[result] %s" % result)


# Use this method when you do not care for fields from parent table
def print_error(msg):
    error = {"has_error": True, "error": msg}
    print("[result] %s" % json.dumps(error))


def format_success(event_dict=None):
    """
    Creates or updates an event dict to include the standard 'error' and 'has_error' fields with default values

    Args:
        event_dict (dict): Optional input to pass a dict of existing results to update. If none is provided, a dict
            containing only the new default fields will be returned.

    Returns:
        dict: New or updated dict containing default 'error' and 'has_error' keys
    """
    if not isinstance(event_dict, dict):
        event_dict = {"result": event_dict}
    event_dict.update({'error': None, 'has_error': False})
    return event_dict


def format_error(msg, event_dict=None):
    """
    Creates or updates an event dict to include the standard 'error' and 'has_error' fields for error results

    Args:
        msg (str): Error message string to include in the 'error' field of the output dict
        event_dict (dict): Optional input to pass a dict of existing results to update. If none is provided, a dict
            containing only the new default fields will be returned.

    Returns:
        dict: New or updated dict containing default 'error' and 'has_error' keys for error results

    """
    event_dict = event_dict if event_dict else {}
    event_dict.update({'error': msg, 'has_error': True})
    return event_dict


def print_correlated_error(msg, original_lhub_id, event_dict=None):
    """
    Prints an error result which will be correlated with the original lhub_id. If no dict value for event_dict is
    provided, the JSON event will contain only 'error' and 'has_error' fields.

    Args:
        msg (str): Error message (string) to place in the 'error' field in the JSON LogicHub output
        original_lhub_id (str or int): The lhub_id value from LogicHub source/parent table
        event_dict (dict): Optional dict of existing key-value pairs to include in the JSON LogicHub output

    Returns:
        N/A

    """
    event_dict = event_dict if event_dict else {}
    event_dict = format_error(msg, event_dict)
    meta_data_dict = {"original_lhub_id": original_lhub_id}
    print('[result][meta]{}[/meta]{}'.format(json.dumps(meta_data_dict), json.dumps(event_dict)))


# Function to use while serializing data structure using json.dumps if json contains datetime object.
def serialize_datetime_object(obj):
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


# TODO ideally this would just be print_correlated_result(msg) with the system populating the original_lhub_id
def print_correlated_result(result, original_lhub_id):
    """
    :param result: could be a string or dict
    :param original_lhub_id: Correlation id
    :return:
    """
    meta_data_dict = {"original_lhub_id": original_lhub_id}
    if isinstance(result, dict):
        result = json.dumps(result)
    print('[result][meta]{}[/meta]{}'.format(json.dumps(meta_data_dict), result))


def print_debug_log(msg):
    try:
        print("[Debug] %s" % msg)
    except Exception as err:
        print("[Debug] Unknown exception while trying to print debug log: %s" % repr(err))


def print_successful_validation_result():
    print_result("{}")


def render_jinja_template(template_string, data, autoescape=False):
    if isinstance(template_string, str):
        unicode_template_string = template_string
    else:
        unicode_template_string = str(template_string, "utf-8")

    unicode_data = {}
    for key, value in list(data.items()):
        unicode_data[key] = value

    # undefined=jinja2.StrictUndefined this tells the parser to throw error if some variable is used in template but,
    # its value is not passed in the context environment
    jinja2_template = jinja2.Template(unicode_template_string, autoescape=autoescape, undefined=jinja2.StrictUndefined)
    return jinja2_template.render(unicode_data)


def convert_milliseconds_to_seconds(milliseconds):
    return milliseconds * 1.0 / 1000.0


def check_for_http_or_https_protocol(url):
    """ Checks for http:// or https:// protocol
        returns True if URL does NOT begin with http:// or https://
    """
    return url[:8] != "https://" and url[:7] != "http://"


def add_default_http_protocol_if_missing(url, protocol="http"):
    """ checks url for http protocol, adds a default http protocol if missing """
    if check_for_http_or_https_protocol(url):
        return protocol + "://" + url
    else:
        return url


def create_url_params_from_list(param_list):
    url_param_string = ''
    for url_param in param_list:
        if not url_param_string:
            url_param_string = '?'
        else:
            url_param_string = url_param_string + '&'
        url_param_string = url_param_string + str(url_param)
    return url_param_string


# Get a nested key from a dict, without having to do loads of ifs
def get_nested_key_value(results, keys):
    if isinstance(keys, list) and len(keys) > 0:

        if isinstance(results, dict) or isinstance(results, OrderedDict):
            key = keys.pop(0)
            if key in results:
                return get_nested_key_value(results[key], keys)
            else:
                return None
        else:
            if isinstance(results, list) and len(results) > 0:
                return get_nested_key_value(results[0], keys)
            else:
                return results
    else:
        return results


def print_each_result_in_list(results, original_lhub_id=None, return_result_in_json_format=True, encoder=str, ensure_ascii=True):
    if not results:
        if not original_lhub_id:
            return print_result(format_success({"noResults": "no results returned"}))
        else:
            return print_correlated_result(format_success({"noResults": "no results returned"}), original_lhub_id)
    for result in results:
        if return_result_in_json_format:
            result = json.dumps(format_success(result), default=encoder, sort_keys=True, ensure_ascii=ensure_ascii)
        if original_lhub_id is None:
            print_result(result)
        else:
            print_correlated_result(result, original_lhub_id)


def random_text(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


"""
@param size: length of random password desired
@param rules: array/dict of dicts. 
    Eg: [{"character_set": "1234567890", "size": 5}, {"character_set": "!@", "size": 5}]
    or
    {
        "alphabets": {"character_set": "abcdefghijklmnopqrstuvwxyz", "size": 5},
        "numbers": {"character_set": "1234567890", "size": 5},
        "special characters": {"character_set": "!@", "size": 5}
    }
@return: password string of length 'size'
"""
def password_generator(size, rules):
    password = ""

    if isinstance(rules, dict):
        rules = [rule for rule in rules.values()]
    for rule in rules:
        password += ''.join(random.choice(rule['character_set']) for _ in range(rule['size']))

    if len(password) > size:
        raise Exception("Invalid Password Rules")
    else:
        password_arr = list(password)
        for _ in range(len(password), size):
            password_arr.append(random.choice(password))
        random.shuffle(password_arr)
        return ''.join(password_arr)


def xstr(s):
    return None if s is None else str(s)


def string_or_none(s):
    if s:
        return s
    else:
        return None


def array_or_none(s):
    if s:
        try:
            return json.loads(s)
        except:
            return [s]
    else:
        return None


def int_of_string_or_none(s):
    if s:
        return int(s)
    else:
        return None


def keep_retrying(pull, check, sleep):
    r = pull()
    if check(r):
        return r
    else:
        time.sleep(sleep)
        return keep_retrying(pull, check, sleep)


def convert_xml_attr_string_in_json_to_json_property(json_obj, attr, custom_name=''):
    if not attr.startswith('@'):
        return json_obj
    new_key = custom_name if custom_name else attr[1:]
    json_obj[new_key] = json_obj[attr]
    del json_obj[attr]
    return json_obj


# helper function used in actions which are processed through Integration.process_multiple_rows_with_duplicate_columns
# Sometimes, we want a common msg/errorMsg for all rows in bucket supplied, so use this function in such cases.
def all_message_response_map(bucket, success, msg=""):
    result = {}
    for column_values in bucket:
        result[column_values["original_tuple"]] = success, msg
    return result


def get_remaining_time_for_action(start_time, timeout):
    time_elapsed = time.time() - start_time
    if time_elapsed < timeout:
        return timeout - time_elapsed
    else:
        return 0


def ip_address_as_string(ip_addr):
    try:
        return str(netaddr.IPAddress(ip_addr))
    except:
        return None


def ip_address_as_long(ip_addr):
    try:
        return int(netaddr.IPAddress(ip_addr))
    except:
        return None


def get_execution_time_range():
    start_datetime = __get_stripped_env_float(global_constants.EXECUTION_START_TIME) / 1000.0
    start_datetime = datetime.datetime.fromtimestamp(start_datetime, dateutil.tz.UTC)
    end_datetime = __get_stripped_env_float(global_constants.EXECUTION_END_TIME) / 1000.0
    end_datetime = datetime.datetime.fromtimestamp(end_datetime, dateutil.tz.UTC)
    return {"start_datetime": start_datetime, "end_datetime": end_datetime}
