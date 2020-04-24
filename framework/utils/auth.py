import string
import secrets
from random import choice
from user.models import User


class AuthEmailBackend:
    @staticmethod
    def authenticate(request, username=None, password=None, **kwargs):
        if username is not None:
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
            else:
                if user.check_password(password) and user.is_active:
                    return user
        return None


def generate_unique_username(username):
    try:
        User.objects.get(username=username)
        generatedUsername = username + ''.join([choice(string.digits) for i in range(3)])
        return generate_unique_username(generatedUsername)
    except User.DoesNotExist:
        return username


def generate_username_from_email(email):
    try:
        emailUsername = email.split('@')[0]
        return generate_unique_username(emailUsername)
    except IndexError:
        raise Exception("Invalid Email")


def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(10))
