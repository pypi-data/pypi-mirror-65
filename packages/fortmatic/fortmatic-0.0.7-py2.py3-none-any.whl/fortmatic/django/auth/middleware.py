from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from fortmatic.django.config import FORTMATIC_AUTH_BACKEND
from fortmatic.django.config import FORTMATIC_IDENTITY_KEY
from fortmatic.django.exceptions import UnableToLoadUserFromIdentityToken
from fortmatic.errors import DIDTokenCanotBeUsedRightNow
from fortmatic.errors import DIDTokenHasExpired
from fortmatic.errors import InvalidIdentityToken
from fortmatic.errors import InvalidSignerAddress
from fortmatic.utils.auth import get_identity_token_from_header
from fortmatic.utils.auth import PhantomAuth


user_model = get_user_model()


class FortmaticAuthMiddleware(MiddlewareMixin):

    @staticmethod
    def _persist_data_in_session(request, identity_token):
        request.session[FORTMATIC_IDENTITY_KEY] = identity_token
        request.session.modified = True

    @staticmethod
    def _load_identity_token_from_session(request):
        return request.session.get(FORTMATIC_IDENTITY_KEY, None)

    @staticmethod
    def _load_identity_token_from_header(request):
        return get_identity_token_from_header(request)

    @staticmethod
    def _is_request_related_to_fortmatic(identity_token):
        return identity_token is not None

    @staticmethod
    def _try_loading_user_from_identity_token(identity_token):
        public_address = PhantomAuth().get_public_address(identity_token)

        try:
            return user_model.get_by_public_address(public_address)
        except user_model.DoesNotExist:
            return AnonymousUser()

    @staticmethod
    def can_user_be_logged_in(user):
        if user is None:
            return False

        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def _attempt_handling_anonymous_user(self, request, identity_token):
        user = self._try_loading_user_from_identity_token(identity_token)

        if not user.is_anonymous and self.can_user_be_logged_in(user):
            # Log the user in to rehydrate the session.
            login(request, user, backend=FORTMATIC_AUTH_BACKEND)
        else:
            raise UnableToLoadUserFromIdentityToken()

    def _load_identity_token_from_sources(self, request):
        # The identity token from header take precedence over the one in session.
        return self._load_identity_token_from_header(
            request,
        ) or self._load_identity_token_from_session(request)

    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The Fortmatic authentication middleware requires authentication '
            'middleware to be installed. Edit your MIDDLEWARE setting to insert '
            '`django.contrib.auth.middleware.AuthenticationMiddleware` before '
            '`fortmatic.django.auth.middleware.FortmaticAuthMiddleware`.'
        )

        identity_token = self._load_identity_token_from_sources(request)

        if not self._is_request_related_to_fortmatic(identity_token):
            return

        try:
            PhantomAuth().validate_token(identity_token)
        except (
            InvalidIdentityToken,
            InvalidSignerAddress,
            DIDTokenHasExpired,
            DIDTokenCanotBeUsedRightNow,
        ):
            logout(request)
            return

        if request.user.is_anonymous:
            try:
                self._attempt_handling_anonymous_user(request, identity_token)
            except UnableToLoadUserFromIdentityToken:
                return

        if (
            request.user.public_address and
            request.user.public_address != PhantomAuth().get_public_address(
                identity_token,
            )
        ):
            logout(request)
            return

        if self.can_user_be_logged_in(request.user):
            self._persist_data_in_session(request, identity_token)
