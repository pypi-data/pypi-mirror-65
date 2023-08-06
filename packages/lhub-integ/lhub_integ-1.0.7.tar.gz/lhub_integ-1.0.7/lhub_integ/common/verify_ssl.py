import urllib3
import os

from lhub_integ.common.constants import *
from lhub_integ.common.input_helpers import _get_stripped_env_string


def verify_ssl_enabled(ssl_verify_default='True'):
    return _get_stripped_env_string(SSL_VERIFY_KEY, ssl_verify_default) != 'False'


if not verify_ssl_enabled():
    # Setting the path to CA cert empty, then it won't verify SSL certificate.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    os.environ.__setitem__(PATH_TO_CA_CERT, '')

