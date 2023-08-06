import time


def handle_request_throttling(wait_time_in_millis, req_func, max_retries=1):
    """
    This function handles throttling of request, it waits for specified time and retries.
    :param wait_time_in_millis:
    :param req_func: request function that returns response object. e.g lambda : requests.get("www.example.com")
    :param max_retries: default = 1,
    :return: response
    """
    assert max_retries >= 0, "Invalid max_retries argument: '{}', value must be non negative".format(max_retries)
    response = req_func()
    while response.status_code == 429 and max_retries:
        time.sleep(wait_time_in_millis / 1000.0)
        response = req_func()
        max_retries -= 1

    return response
