from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'phone_number', 'country', 'birthdate')



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Email or password is incorrect")
        data['user'] = user
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        user = authenticate(
            email=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError("Email or password is incorrect")
        data = super().validate(attrs)
        return data
    

class ChangePasswordSerializer(serializers.Serializer):   
    new_password = serializers.CharField(write_only=True)    
    renew_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['renew_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data