from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """Выполняет аутентификацию пользователя по email"""
    def authenticate(self):
