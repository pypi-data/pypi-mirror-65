from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from fortmatic.django.config import FortmaticAuthBackendMode
from fortmatic.django.exceptions import MissingAuthorizationHeader
from fortmatic.django.exceptions import MissingUserEmailInput
from fortmatic.django.exceptions import PublicAddressDoesNotExist
from fortmatic.django.exceptions import UnsupportedAuthMode
from fortmatic.django.exceptions import UserEmailMissmatch
from fortmatic.errors import DIDTokenCanotBeUsedRightNow
from fortmatic.errors import DIDTokenHasExpired
from fortmatic.errors import InvalidIdentityToken
from fortmatic.errors import InvalidSignerAddress
from fortmatic.utils.auth import get_identity_token_from_header
from fortmatic.utils.auth import PhantomAuth
from fortmatic.utils.logging import log_debug
from fortmatic.utils.logging import log_info


user_model = get_user_model()


class FortmaticAuthBackend(ModelBackend):

    @staticmethod
    def _load_user_from_email(email):
        log_debug('Loading user by email.', email=email)
        try:
            return user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None

    @staticmethod
    def _validate_identity_token_and_load_user(
        identity_token,
        email,
        public_address,
    ):
        try:
            PhantomAuth().validate_token(identity_token)
        except (
            InvalidIdentityToken,
            InvalidSignerAddress,
            DIDTokenHasExpired,
            DIDTokenCanotBeUsedRightNow,
        ) as e:
            log_debug(
                'DID Token failed validation. No user is to be retrieved.',
                error_class=e.__class__.__name__,
            )
            return None

        try:
            user = user_model.get_by_public_address(public_address)
        except user_model.DoesNotExist:
            raise PublicAddressDoesNotExist()

        if user.email != email:
            raise UserEmailMissmatch()

        return user

    def user_can_authenticate(self, user):
        if user is None:
            return False

        return super().user_can_authenticate(user)

    def _update_user_with_public_address(self, user, public_address):
        if self.user_can_authenticate(user):
            user.update_user_with_public_address(
                user_id=None,
                public_address=public_address,
                user_obj=user,
            )

    def _handle_phantom_auth(self, request, email):
        identity_token = get_identity_token_from_header(request)
        if identity_token is None:
            raise MissingAuthorizationHeader()

        public_address = PhantomAuth().get_public_address(identity_token)

        try:
            user = self._validate_identity_token_and_load_user(
                identity_token,
                email,
                public_address,
            )
        except PublicAddressDoesNotExist:
            user = self._load_user_from_email(email)
            if user is None:
                log_debug(
                    'User is not authenticated. No user found with the given email.',
                    email=email,
                )
                PhantomAuth().logout(public_address)
                return

            self._update_user_with_public_address(user, public_address)
        except UserEmailMissmatch as e:
            log_debug(
                'User is not authenticated. User email does not match for the '
                'public address.',
                email=email,
                public_address=public_address,
                error_class=e.__class__.__name__,
            )
            PhantomAuth().logout(public_address)
            return

        if self.user_can_authenticate(user):
            log_info('User authenticated with DID Token.')
            return user

    def authenticate(
        self,
        request,
        user_email=None,
        mode=FortmaticAuthBackendMode.PHANTOM,
    ):
        if not user_email:
            raise MissingUserEmailInput()

        user_email = user_model.objects.normalize_email(user_email)

        if mode == FortmaticAuthBackendMode.PHANTOM:
            return self._handle_phantom_auth(request, user_email)
        else:
            raise UnsupportedAuthMode()
