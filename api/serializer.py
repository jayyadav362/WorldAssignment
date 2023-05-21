from rest_framework import serializers
from account.models import *


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'email', 'phone_number']


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=10)


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)