from abc import ABC

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login, User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Posts, BlackListedToken

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "post_title", "post_description"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    token = serializers.CharField(max_length=200, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = get_user_model()
        try:
            user_ex = user.objects.get(email=email)
        except user_ex.DoesNotExist:
            raise serializers.ValidationError("User not exist in this email.")
        else:
            if user_ex.check_password(password):
                    payload = JWT_PAYLOAD_HANDLER(user_ex)
                    jwt_token = JWT_ENCODE_HANDLER(payload)
                    update_last_login(None, user_ex)
                    return {
                        'email': user_ex.email,
                        'token':jwt_token
                    }
            else:
                raise serializers.ValidationError("User with given password does not exists")


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackListedToken
        fields = ['token', 'user_id']

