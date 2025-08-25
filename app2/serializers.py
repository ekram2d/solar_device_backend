from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, Devices,CustomUser,BankInformation,BrandInformation,DeviceInformation,DeviceLocation
import uuid
from rest_framework.response import Response
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if not data.get('terms_and_conditions'):
            raise serializers.ValidationError("You must accept the terms and conditions.")
        return data

    def create(self, validated_data):
        print("Creating user with validated data:", validated_data)
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        # Auto-generate a unique username (can be from phone or random UUID)
        # print("Creating user with email:", email)
        # print("Creating user with phone:", validated_data.get('phone_number', ''))
        # print("Creating user with first name:", first_name)
        # print("Creating user with last name:", last_name)
        phone = validated_data.get('phone_number', '')
        username = f"{first_name.lower()}.{last_name.lower()}.{phone[-4:]}"  # example format

        # Create Django user
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        print('user.save()',user)
        # Link user to CustomUser
        custom_user = CustomUser.objects.create(user=user, **validated_data)
        return custom_user

# class SolarDeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Devices
#         fields = '__all__'
class SolarDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = '__all__'

    def validate(self, data):
        user = data.get('user')
        name = data.get('name')

        if Devices.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError("❌ You already added a device with this name.")
        return data
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class BankInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankInformation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'custom_user']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        custom_user = getattr(user, 'custom_user_app2', None)

        if not custom_user:
            raise serializers.ValidationError("Custom user does not exist.")

        # Prevent duplicate account_number for the same user
        account_number = data.get('account_number')
        if BankInformation.objects.filter(custom_user=custom_user, account_number=account_number).exists():
            raise serializers.ValidationError("This bank account is already added.")

        return data


class BrandDevicesSerializer(serializers.ModelSerializer):
    brand_image = serializers.SerializerMethodField()

    class Meta:
        model = BrandInformation
        fields = ['id', 'brand_name', 'brand_image']

    def get_brand_image(self, obj):
        request = self.context.get('request')
        if obj.brand_image and hasattr(obj.brand_image, 'url'):
            return request.build_absolute_uri(obj.brand_image.url)
        return None

    def create(self, validated_data):
        # Serializer handles saving, no request here
        return BrandInformation.objects.create(**validated_data)
class DeviceInformationSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand_info.brand_name", read_only=True)
    brand_image = serializers.ImageField(source="brand_info.brand_image", read_only=True)
    signature = serializers.SerializerMethodField()

    class Meta:
        model = DeviceInformation
        fields = [
            'id',
            'user',
            'custom_user',
            'device_type',
            'capacity',
            'operations_date',
            'brand_info',
            'brand_name',
            'brand_image',
            'signature',
        ]

    def get_signature(self, obj):
        request = self.context.get('request')
        if obj.signature:
            return request.build_absolute_uri(obj.signature.url)
        return None

class DeviceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLocation
        fields='__all__'