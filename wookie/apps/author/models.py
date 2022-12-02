from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=255)

