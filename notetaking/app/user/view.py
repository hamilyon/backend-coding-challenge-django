import json

from app.user.model import auth_service
from django.http import HttpResponse


def login(request):
    json_data = json.loads(request.body)
    username, password = [json_data.get(it) for it in ["username", "password"]]
    auth_service.login(request, username, password.encode('utf-8'))
    return HttpResponse("the cookie has been set", status=200)


def logout(request):
    auth_service.logout()
    return HttpResponse(status=200)
