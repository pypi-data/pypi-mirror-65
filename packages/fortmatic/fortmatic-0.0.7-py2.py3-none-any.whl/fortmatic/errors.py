class FortmaticErrorBase(Exception):
    pass


class InvalidSignerAddress(FortmaticErrorBase):
    pass


class InvalidIdentityToken(FortmaticErrorBase):
    pass


class DIDTokenHasExpired(FortmaticErrorBase):
    pass


class DIDTokenCanotBeUsedRightNow(FortmaticErrorBase):
    pass
