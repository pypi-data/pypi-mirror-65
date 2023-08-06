import base64
import json

from eth_account.messages import encode_defunct
from web3.auto import w3

from fortmatic.api_resources.auth.user import user_logout_v1
from fortmatic.errors import DIDTokenCanotBeUsedRightNow
from fortmatic.errors import DIDTokenHasExpired
from fortmatic.errors import InvalidIdentityToken
from fortmatic.errors import InvalidSignerAddress
from fortmatic.utils.http import parse_authorization_header
from fortmatic.utils.time import apply_nbf_grace_period
from fortmatic.utils.time import epoch_time_now


def get_identity_token_from_header(request):
    return parse_authorization_header(request)


def parse_public_address(input_str):
    return input_str.split(':')[-1]


class PhantomAuth:

    @staticmethod
    def decode_token(identity_token):
        """
        Args:
            identity_token (base64.str): Base64 encoded string.

        Raises:
            InvalidIdentityToken: If token is malformed.
        """
        try:
            decoded_dat = json.loads(
                base64.urlsafe_b64decode(
                    identity_token,
                ).decode('utf-8'),
            )
        except Exception:
            raise InvalidIdentityToken()

        proof = decoded_dat[0]
        claims = decoded_dat[1]

        return proof, claims

    def validate_token(self, identity_token):
        """
        Args:
            identity_token (base64.str): Base64 encoded string.

        Returns:
            None.
        """
        proof, claims = self.decode_token(identity_token)
        signable_message = encode_defunct(text=claims)
        recovered_address = w3.eth.account.recover_message(
            signable_message,
            signature=proof,
        )

        claims = json.loads(claims)
        current_time_in_s = epoch_time_now()

        if recovered_address != parse_public_address(claims['iss']):
            raise InvalidSignerAddress()

        if current_time_in_s > claims['ext']:
            raise DIDTokenHasExpired()

        if current_time_in_s < apply_nbf_grace_period(claims['nbf']):
            raise DIDTokenCanotBeUsedRightNow()

        # TODO(ajen#42|2020-01-29): Need to do the last validation on the aud.

        return claims

    def get_public_address(self, identity_token):
        """
        Args:
            identity_token (base64.str): Base64 encoded string.

        Raises:
            InvalidIdentityToken: If token is malformed.
        """
        _, claims = self.decode_token(identity_token)
        claims = json.loads(claims)

        try:
            return parse_public_address(claims['iss'])
        except KeyError:
            raise InvalidIdentityToken()

    def logout(self, public_address):
        user_logout_v1(public_address)
