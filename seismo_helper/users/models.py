from django.db import models
from django.contrib.auth.models import AbstractUser
from backend.models import Corporation


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    second_name = models.CharField('first name', max_length=150, blank=True)
    third_name = models.CharField('first name', max_length=150, blank=True)
    # USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    corporation = models.ForeignKey(
        Corporation,
        on_delete=models.PROTECT,
        related_name="users",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.email
