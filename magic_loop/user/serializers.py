from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CreateUserSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "verify_password"]

    def validate(self, attrs):
        password = attrs.get('password')
        verify_password = attrs.get('verify_password')
        if password != verify_password:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
