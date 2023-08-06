class FortmaticDjangoException(Exception):
    pass


class UnsupportedAuthMode(FortmaticDjangoException):
    pass


class PublicAddressDoesNotExist(FortmaticDjangoException):
    pass


class UserEmailMissmatch(FortmaticDjangoException):
    pass


class MissingUserEmailInput(FortmaticDjangoException):
    pass


class MissingAuthorizationHeader(FortmaticDjangoException):
    pass


class UnableToLoadUserFromIdentityToken(FortmaticDjangoException):
    pass
