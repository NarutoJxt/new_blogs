from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import BlogUser


class UserRegisterSerializer(ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserRegisterSerializer, self).create(validated_data)

    class Meta:
        model = BlogUser
        fields = ["username","password","email"]

class UserLoginSerializer(ModelSerializer):

    class Meta:
        model = BlogUser
        fields = ["username","password"]