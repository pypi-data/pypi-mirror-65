import os
import jinja2
import datetime

from lhub_integ.common import helpers
from lhub_integ.common.input_helpers import _get_stripped_env_string, _get_stripped_env_json, _get_stripped_env_yaml
from lhub_integ.common.input_helpers import _get_safe_stripped_env_integer, _get_json_from_string
from lhub_integ.common.query_parser import validate_and_parse, generate_query
import yaml.parser

# check_... methods return an error object if the given value is invalid
# validate_... methods additionally print the final result or exit


def create_error(msg, input_id=''):
    """
    Format an error response for validation of integration instances and actions

    Args:
        msg (str/unicode): Message to present to the user
        input_id (str): The environment variable name (what the variable is called in the descriptor and in inputs.py)

    Returns:
        (dict): Message and field ID to return to the user

    """
    return {"message": msg, "inputId": input_id}


def check_input_value_in_list_of_values(fieldname, input_id, list_of_values):
    value = _get_stripped_env_string(input_id)
    if not value:
        return create_error("{0} cannot be empty.".format(fieldname), input_id)
    elif value not in list_of_values:
        return create_error(
            "{0} is an invalid value. Must be one of: ({1}).".format(value, ', '.join(list_of_values)),
            input_id
        )
    else:
        return None


def check_optional_value_in_list_of_values(fieldname, input_id, list_of_values):
    value = _get_stripped_env_string(input_id)
    if not value:
        return None
    else:
        return check_input_value_in_list_of_values(fieldname, input_id, list_of_values)


def check_string(fieldname, value, input_id):
    """
    Check whether a given variable contains a value, and return a formatted error for integration input validation if it
    is empty.

    Args:
        fieldname (str): What it's called for the user
        value (str): The value entered by the user
        input_id (str): The environment variable name (what the variable is called in the descriptor and in inputs.py)

    Returns:
        None or a formatted validation error

    """
    if not value:
        return create_error("{0} cannot be empty.".format(fieldname), input_id)
    else:
        return None


def check_nonempty_string(input_id):
    value = _get_stripped_env_string(input_id)
    if not value:
        return create_error("Field cannot be empty.", input_id)
    else:
        return None


def check_nonempty_strings(*input_ids):
    for input_id in input_ids:
        value = _get_stripped_env_string(input_id)
        if not value:
            return create_error("Field cannot be empty.", input_id)
    return None


def check_non_negative_integer(input_id, value):
    try:
        intval = int(value)
        if intval < 0:
            return create_error("Invalid value ({0}), expected non-negative number".format(value), input_id)
        else:
            return None
    except ValueError:
        return create_error("Invalid value ({0}), expected integer".format(value), input_id)


def check_positive_integer(input_id, value):
    try:
        intval = int(value)
        if intval <= 0:
            return create_error("Invalid value ({0}), expected positive number".format(value), input_id)
        else:
            return None
    except ValueError:
        return create_error("Invalid value ({0}), expected integer".format(value), input_id)


def check_ranged_integer(input_id, value, minimum, maximum):
    error_msg = "Invalid value ({0}), expected a number between {1} and {2}".format(value, minimum, maximum)
    try:
        intval = int(value)
        if not(minimum <= intval <= maximum):
            return create_error(error_msg, input_id)
        else:
            return None
    except ValueError:
        return create_error(error_msg, input_id)


def check_optional_ranged_integer(input_id, minimum, maximum):
    value = _get_stripped_env_string(input_id)
    if value:
        return check_ranged_integer(input_id, value, minimum, maximum)
    else:
        return None


def check_non_negative_float(input_id, value):
    try:
        _var = float(value)
        if _var < 0:
            return create_error(
                "Invalid value ({0}), expected a non-negative number (whole or decimal)".format(value), input_id)
        else:
            return None
    except ValueError:
        return create_error(
            "Invalid value ({0}), expected a non-negative number (whole or decimal)".format(value), input_id)


def check_optional_non_negative_float(input_id):
    value = _get_stripped_env_string(input_id)
    if value:
        return check_non_negative_float(input_id, value)
    else:
        return None


def check_valid_json(*input_ids):
    try:
        for i in input_ids:
            value = _get_stripped_env_json(i)
        return None
    except ValueError:
        return create_error("Invalid value, expected json", i)


def check_valid_and_non_empty_yaml(*input_ids):
    try:
        for i in input_ids:
            value = _get_stripped_env_yaml(i)
            if not value:
                return create_error("Yaml shouldn't be empty", i)
        return None
    except yaml.parser.ParserError:
        return create_error("Invalid value, expected yaml", i)


def check_valid_templated_json(*input_ids):
    try:
        for input_id in input_ids:
            json_string = _get_stripped_env_string(input_id)
            validation_message, parsed_query_template_list = validate_and_parse(json_string)
            if validation_message:
                return create_error("Invalid value ({0})".format(validation_message), input_id)
            dummy_data = {}
            for template in parsed_query_template_list:
                if template[0] == 'VAR':
                    dummy_data[template[1]] = 123 # we are just passing a magic no to pass the validation
            query = generate_query(parsed_query_template_list, dummy_data)
            _get_json_from_string(query)
        return None
    except ValueError:
        return create_error("Invalid value ({0}), expected json".format(json_string), input_id)


def check_valid_templated_strings(*input_ids):
    try:
        for input_id in input_ids:
            json_string = _get_stripped_env_string(input_id)
            validation_message, parsed_query_template_list = validate_and_parse(json_string)
            if validation_message:
                return create_error("Invalid value ({0})".format(validation_message), input_id)
            dummy_data = {}
            for template in parsed_query_template_list:
                if template[0] == 'VAR':
                    dummy_data[template[1]] = 123 # we are just passing a magic no to pass the validation
            generate_query(parsed_query_template_list, dummy_data)
        return None
    except:
        return create_error("Invalid value ({0}), expected valid string".format(json_string), input_id)


def check_valid_template_string(input_id, accept_empty=False):
    template_content = _get_stripped_env_string(input_id)
    if not template_content and not accept_empty:
        return create_error("Template content cannot be empty.", input_id)

    if not template_content and accept_empty:
        return None
    try:
        if isinstance(template_content, str):
            unicode_template_content = template_content
        else:
            unicode_template_content = str(template_content, "utf-8")
        jinja2.Template(unicode_template_content)
    except jinja2.exceptions.TemplateSyntaxError as e:
        error_message = 'Syntax error on line {}: {}'.format(e.lineno, e.message)
        return create_error(error_message, input_id)
    else:
        return None


def check_allowed_options(input_id, field_name, options):
    value = _get_stripped_env_string(input_id)
    if not value:
        return create_error("Field '%s' cannot be empty" % field_name, input_id)
    elif value not in options:
        return create_error(
            "Field '%s' is invalid. Allowed options: %s" % (field_name, options), input_id)
    else:
        return None


def check_optional_non_negative_integer_field(input_id):
    value = _get_stripped_env_string(input_id)
    if value:
        return check_non_negative_integer(input_id, value)
    else:
        return None


def check_optional_date_time_format(input_id, format):
    value = _get_stripped_env_string(input_id)
    if value:
        try:
            datetime.datetime.strptime(value, format)
        except ValueError:
            return create_error("Invalid value ({0}) is not in expected format".format(value), input_id)
    else:
        return None


def check_url(input_id, value):
    from urllib.parse import urlparse
    try:
        urlparse(value)
    except:
        return create_error("Invalid value ({0}), expected URL".format(value), input_id)

    if helpers.check_for_http_or_https_protocol(value):
        return create_error("Invalid value ({0}), expected URL with http or https protocol".format(value), input_id)
    else:
        return None


def check_optional_url_field(input_id):
    value = _get_stripped_env_string(input_id)
    if value:
        return check_url(input_id, value)
    else:
        return None


def flatten(list_with_nones):
    if list_with_nones:
        return [_f for _f in list_with_nones if _f is not None]
    else:
        return list_with_nones


def check_column_name_and_delay(colname_var, timedelay_var):
    column_name = _get_stripped_env_string(colname_var)
    time_between_request = _get_stripped_env_string(timedelay_var)

    errors_with_nones = []

    errors_with_nones.append(check_string(
        "Column Name", column_name, colname_var))

    if time_between_request:
        errors_with_nones.append(check_non_negative_integer(
            timedelay_var, time_between_request))

    return flatten(errors_with_nones)


def check_column_name(colname_var):
    column_name = _get_stripped_env_string(colname_var)
   
    errors_with_nones = []

    errors_with_nones.append(check_string(
        "Column Name", column_name, colname_var))

    return flatten(errors_with_nones)


def check_column_names(*colnames_var):
    errors_with_nones = []
    for colname_var in colnames_var:
        column_name = _get_stripped_env_string(colname_var)
        errors_with_nones.append(check_string(
            "Column Name", column_name, colname_var))
    return flatten(errors_with_nones)


def check_delay_and_column_names(timedelay_var, *colnames_var):
    errors_with_nones = []
    time_between_request = _get_stripped_env_string(timedelay_var)
    if time_between_request:
        errors_with_nones.append(check_non_negative_integer(
            timedelay_var, time_between_request))
    for colname_var in colnames_var:
        column_name = _get_stripped_env_string(colname_var)
        errors_with_nones.append(check_string(
            "Column Name", column_name, colname_var))
    return flatten(errors_with_nones)


def validate_column_name_and_delay(colname_var, timedelay_var):
    finalize_validation_from_errors(
        check_column_name_and_delay(colname_var, timedelay_var)
    )


def validate_column_name(colname_var):
    finalize_validation_from_errors(
        check_column_name(colname_var)
    )


def validate_column_names(*colnames_var):
    finalize_validation_from_errors(
        check_column_names(*colnames_var)
    )


def validate_delay_and_column_names(timedelay_var, *colnames_var):
    finalize_validation_from_errors(
        check_delay_and_column_names(timedelay_var, *colnames_var)
    )


def validate_optional_api_key(api_key_var):
    api_key = os.environ.get(api_key_var)
    if api_key:
        validate_api_key(api_key_var)
    else:
        helpers.print_successful_validation_result()


def validate_api_key(api_key_var):
    api_key = _get_stripped_env_string(api_key_var)
    error = check_string("API Key", api_key, api_key_var)
    if error:
        helpers.exit_with_instantiation_errors(2, [error])
    else:
        helpers.print_successful_validation_result()


def check_string_params(label_varname_dict):
    errors_with_nones = []
    for label, env_var_name in list(label_varname_dict.items()):
        value = _get_stripped_env_string(env_var_name)
        errors_with_nones.append(check_string(label, value, env_var_name))
    return flatten(errors_with_nones)


def check_key_and_value(key_id, value_id):
    key = _get_stripped_env_string(key_id)
    value = _get_stripped_env_string(value_id)
    if bool(key) != bool(value):
        return create_error("Key and Value both should be entered.", key_id)
    else:
        return None


def validate_string_params(label_varname_dict):
    finalize_validation_from_errors(
        check_string_params(label_varname_dict)
    )


def check_username_password_exist(username_var, password_var):
    return check_string_params({
        "Username": username_var,
        "Password": password_var
    })


def finalize_validation_from_errors(errors):
    errors = flatten(errors)

    # Return results or exit
    if not errors:
        helpers.print_successful_validation_result()
    else:
        helpers.exit_with_instantiation_errors(2, errors)


def validate_username_password(username_var, password_var):
    errors = check_username_password_exist(username_var, password_var)
    finalize_validation_from_errors(errors)


def check_username_password_url(username_var, password_var, url_var):
    return check_string_params({
        "Username": username_var,
        "Password": password_var,
        "Instance URL": url_var,
    })


def check_server_port(server_var, port_var):
    errors = check_string_params({
        "Server": server_var,
        "Port": port_var
    })

    # validate server name
    server_value = _get_stripped_env_string(server_var)
    if ':' in server_value:
        errors.append(create_error("Server name cannot contain protocol", server_var))

    # validate port number, -1 indicates non-integer value given
    port_value = _get_safe_stripped_env_integer(port_var, -1)
    if port_value < 0 or port_value > 65535:
        errors.append(create_error("Port must be between 0 and 65535", port_var))

    return errors


def check_username_password_server_port(username_var, password_var, server_var, port_var):
    errors = check_string_params({
        "Username": username_var,
        "Password": password_var
    })

    if errors:
        return errors
    else:
        return check_server_port(server_var, port_var)


def check_username_apikey(username_var, apikey_var):
    return check_string_params({
        "Username": username_var,
        "API Key": apikey_var
    })


def check_action_timeout(timeout_var='__lh_action_timeout_sec'):
    return check_optional_non_negative_integer_field(timeout_var)


def validate_username_apikey(username_var, apikey_var):
    finalize_validation_from_errors(
        check_username_apikey(username_var, apikey_var)
    )


def validate_single_string(field_name, value, input_id=None):
    finalize_validation_from_errors(
        # a list of errors is expected, can include None
        [check_string(field_name, value, input_id)]
    )
