from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        try:
            custom_user = CustomUser.objects.get(user_id=user_obj.id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(" user  not found.")

        user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        
        refresh = RefreshToken.for_user(user)  # ✅ Define refresh here

        data['user'] = user
        data['custom_user'] = custom_user
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
