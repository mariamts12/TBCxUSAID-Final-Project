from rest_framework import serializers
from .models import User
from .tasks import send_sign_up_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "patterns_count",
            "saved_patterns_count",
            "projects_count",
        ]


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "patterns_count",
            "saved_patterns_count",
            "projects_count",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "verify_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        verify_password = attrs.get("verify_password")
        if password != verify_password:
            raise serializers.ValidationError("Passwords don't match. Try again.")
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()

        send_sign_up_mail.delay(user.email, user.username)
        return user
