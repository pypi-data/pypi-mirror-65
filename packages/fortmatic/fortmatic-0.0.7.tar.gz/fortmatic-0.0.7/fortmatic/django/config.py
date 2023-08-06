FORTMATIC_IDENTITY_KEY = '_fortmatic_identity_token'
FORTMATIC_AUTH_BACKEND = 'fortmatic.django.auth.backends.FortmaticAuthBackend'


class FortmaticAuthBackendMode:

    DJANGO_DEFAULT_AUTH = 0
    PHANTOM = 1

    ALLOWED_MODES = frozenset([DJANGO_DEFAULT_AUTH, PHANTOM])
