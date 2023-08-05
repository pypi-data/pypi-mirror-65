from django.urls import path, include
from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

import requests
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse


def include_auth_urls():
    return include([
        path(r'login/', login),
        path(r'logout/', logout)
    ])


@api_view(["GET"])
@authentication_classes([])
def login(request):
    auth_redirect_url: str = request.build_absolute_uri().split("?")[0]
    # since the app is running in container, no way to know its on ssl
    auth_redirect_url = auth_redirect_url.replace('http', 'https')
    auth_code: str = request.query_params.get("code", "")
    app_redirect_url: str = request.query_params.get("state", "")

    client_id = settings.IDENTITY_CLIENT_ID
    client_secret = settings.IDENTITY_CLIENT_SECRET

    reply = requests.post(
        f"{settings.IDENTITY_HOST}/o/token/",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": auth_redirect_url,
        },
        auth=(client_id, client_secret),
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            auth_redirect_url
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    tokens = reply.json()
    introspect_response = requests.post(
        f"{settings.IDENTITY_HOST}/o/introspect/",
        data={"token": tokens["access_token"],},
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            tokens["access_token"]
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    email = introspect_response.json()["username"]
    # here we can also get additional user info, GUID, etc
    user, _ = User.objects.get_or_create(email=email, username=email)
    request.session["username"] = email

    return HttpResponseRedirect(redirect_to=app_redirect_url)


@api_view(["GET"])
@authentication_classes([])
def logout(request):
    app_redirect_url: str = request.query_params.get("state", "")
    request.session.flush()
    response = HttpResponseRedirect(redirect_to=app_redirect_url)
    response.delete_cookie("sso_shared_session")
    return response
