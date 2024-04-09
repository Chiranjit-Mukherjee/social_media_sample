# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import FriendRequest



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Check if the provided email is a valid email address.
        """
        if not value:
            raise serializers.ValidationError('Email address is required')
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError('Email address is already in use')
        except User.DoesNotExist:
            pass

        return value

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['email'], 
                                        email=validated_data['email'], 
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class UserSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(max_length=100)


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'