from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    # corporation = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "first_name",
            "second_name",
            "third_name",
            "corporation",
            "bio",
            "id"
        )
        read_only_fields = (settings.LOGIN_FIELD,)
