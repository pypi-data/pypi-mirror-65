from rest_framework import authentication
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import exceptions
import requests


class IdentityAuthentication(authentication.BaseAuthentication):
    """
    This should be the first authentication that user goess through, since we always trust the local sessions
    So that we dont have to spam api requests to id service
    """

    def authenticate(self, request):
        username = request.session.get("username")
        if not username or username not in settings.IDENTITY_WHITELIST:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")
        return (user, None)



class IdentitySSOAuthentication(authentication.BaseAuthentication):
    """
    This should be the second authentication that a request goess through:
    When the user doesnt have the local session, we can see if the user has an active session with the id service
    and create local session based on that
    """

    def authenticate(self, request):
        shared_cookie = request.COOKIES.get("sso_shared_session")
        if not shared_cookie:
            # auth not attempted
            return None
        user_info_reply = requests.post(
            f"{settings.IDENTITY_HOST}/auth/validate_sso_session/",
            json={"sso_session_cookie": shared_cookie},
        )

        try:
            user_info_reply.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = (
                "User info request failed",
                e.response.status_code,
                e.response.content,
            )
            raise exceptions.AuthenticationFailed(message)
        user_info = user_info_reply.json()
        user, _ = User.objects.get_or_create(username=user_info["user"]["username"])
        request.session["username"] = user.username
        return (user, None)
