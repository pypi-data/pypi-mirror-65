import os
import json
import yaml


def safe_strip(value):
    if value:
        return value.strip()
    else:
        return value


# Strips whitespaces and attempts to parse integer from environment variable
# Or returns default value if no value is provided
# NOT SAFE against parsing failure for non-integers, will throw a ValueError
def __get_stripped_env_integer(env_var, default=0):
    assert (type(default) == int), "Default value must be an int"
    raw_value = os.environ.get(env_var)
    stripped_value = safe_strip(raw_value)
    if stripped_value:
        return int(stripped_value)
    else:
        return default


# Strips whitespaces and attempts to parse float from environment variable
# Or returns default value if no value is provided
# NOT SAFE against parsing failure for non-float or non integer, will throw a ValueError
def __get_stripped_env_float(env_var, default=0.0):
    if type(default) is int:
        default = float(default)
    else:
        assert (type(default) == float), "Default value must be a float"
    raw_value = os.environ.get(env_var)
    stripped_value = safe_strip(raw_value)
    if stripped_value:
        return float(stripped_value)
    else:
        return default


# Safe version of __get_stripped_env_integer
def _get_safe_stripped_env_integer(env_var, default=0):
    try:
        return __get_stripped_env_integer(env_var, default)
    except:
        return default


# Use in place of os.environ.get()
def _get_stripped_env_string(env_var, default=""):
    raw_value = os.environ.get(env_var)
    stripped_value = safe_strip(raw_value)
    return stripped_value if stripped_value else default


# Use in place of os.environ.get()
def _get_stripped_env_json(env_var, default={}):
    raw_value = os.environ.get(env_var)
    stripped_value = safe_strip(raw_value)
    return json.loads(stripped_value) if stripped_value else default


def _get_stripped_env_yaml(env_var, default=""):
    raw_value = os.environ.get(env_var)
    stripped_value = safe_strip(raw_value)
    return yaml.load(stripped_value) if stripped_value else default


def _get_json_from_string(raw_value, default={}):
    stripped_value = safe_strip(raw_value)
    return json.loads(stripped_value) if stripped_value else default


# Separates comma-separated input into a list of str
# with each element having trailing and leading whitespace removed
# Tolerant to list notation of square brackets
# Examples:
#   None         ->  []
#   '[1,2,3]'    ->  ['1', '2', '3']
#   'a,b,   c  ' ->  ['a', 'b', 'c']
def eval_to_stripped_list(input_str, delimiter=','):
    if not input_str:
        return []
    else:
        input_str_stripped = input_str.lstrip('[').rstrip(']')
        str_list = input_str_stripped.split(delimiter)
        return list(map(safe_strip, str_list))


def eval_to_stripped_list_or_none(input_str, delimiter=','):
    if not input_str:
        return None
    else:
        input_str_stripped = input_str.lstrip('[').rstrip(']')
        str_list = input_str_stripped.split(delimiter)
        return list(map(safe_strip, str_list))
