from requests.exceptions import RequestException

import fortmatic
from fortmatic.api_resources.config import RESOURCE_SERVER
from fortmatic.api_resources.config import SECRET_API_KEY_HEADER


def get_call_uri(resource):
    return RESOURCE_SERVER + resource


def get_secret_api_key_headers():
    if fortmatic.secret_key is None:
        raise Exception(
            'Please specify your account\'s secret key. You can get a secret '
            'key from Fortmatic Dashboard (https://dashboard.fortmatic.com). '
            'And in your application you can do: \n'
            '\t"import fortmatic; fortmatic.secret_key = \'sk_live_XYZ\'"',
        )

    return {SECRET_API_KEY_HEADER: fortmatic.secret_key}


def retry_on_request_exceptions(exception):
    return isinstance(exception, RequestException)
