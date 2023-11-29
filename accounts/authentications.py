from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q

User= get_user_model()

class PhoneBackend(BaseBackend):
    @staticmethod
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(phone_number=username) | Q(email=username)
            )
            print(1)
        except User.DoesNotExist:
            print(2)
            return None

        if user and check_password(password, user.password):
            print(3)
            return user

        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
