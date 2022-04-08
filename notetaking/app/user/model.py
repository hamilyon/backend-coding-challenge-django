import datetime

import bcrypt as bcrypt
from django.db import models


class User(models.Model):
    # using implicit id

    username = models.CharField(max_length=60)
    password_hash = models.BinaryField(max_length=512)
    creation_date = models.DateField(default=datetime.date.today)
    version = models.IntegerField(default=0)

    def to_json(self):
        return {"username": self.username, "id": self.id}


class AuthException(Exception):
    pass


class AuthService():
    def login(self, request, username: str, password: bytes):
        request.session['user'] = self.check_user_password(username, password).to_json()

    def logout(self, request):
        del request.session['user']

    def check_auth(self, request):
        if not request.session.get('user'):
            raise AuthException

    def create_user(self, username: str, password: bytes):
        some_salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password, some_salt)
        user = User(username=username, password_hash=hash)
        user.save()

    def check_user_password(self, username: str, password: bytes):
        user = User.objects.get(username=username)
        result = bcrypt.checkpw(password, user.password_hash)
        if not result:
            raise AuthException()
        return user


auth_service = AuthService()
