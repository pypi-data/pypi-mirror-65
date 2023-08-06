import re

AUTHORIZATION_PATTERN = r'Bearer (?P<token>.+)'


def null_safe(value):
    if value == 'null':
        return None

    return value


def parse_authorization_header(request):
    header_value = request.META.get('HTTP_AUTHORIZATION', '')

    m = re.match(AUTHORIZATION_PATTERN, header_value)

    if m is None:
        return None

    return null_safe(m.group('token'))
