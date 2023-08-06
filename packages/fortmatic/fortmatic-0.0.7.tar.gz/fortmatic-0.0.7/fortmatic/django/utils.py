from django.contrib.auth import logout as django_logout

from fortmatic.utils.auth import PhantomAuth
from fortmatic.utils.logging import log_debug


def logout(request):
    user = request.user

    if not user.is_anonymous and user.public_address:
        PhantomAuth().logout(user.public_address)
        log_debug('Log out user from Fortmatic')

    django_logout(request)
