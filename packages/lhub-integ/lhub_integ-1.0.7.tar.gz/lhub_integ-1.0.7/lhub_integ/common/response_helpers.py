import requests
from lhub_integ.common.helpers import format_success, format_error


# ToDo Duplicate of helpers.format_error
#   Confirm whether this is used anywhere else, switch to the other, and remove from here.
def error_message_json(message):
    return format_error(message)


def derive_result_json(response):
    if response.status_code == 401:
        result = format_error("Authentication failed. Please check the credentials and try again.")

    elif response.status_code == 403:
        result = format_error("Authorization failed. The credentials provided are valid but do not "
                              "have proper access level.")

    elif response.status_code == 404:
        result = format_error("Not found")

    elif response.status_code != requests.codes.ok:
        result = format_error("Unexpected status code %s: %s." % (response.status_code, response.reason))

    else:
        response_json = response.json()
        result = format_success(response_json)
    return result
