from django.contrib.auth.models import AbstractUser


def get_default_restorers(user: AbstractUser):
    return []
