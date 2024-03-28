from account.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterApiSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name", "national_code"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"detail": "passwords must match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class TeacherRegisterApiSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=200, write_only=True)
    school_name = serializers.CharField(required=False)
    biography = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "first_name", "last_name", "national_code", "school_name", "biography"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"detail": "Passwords must match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2")
        school_name = validated_data.pop("school_name", None)
        biography = validated_data.pop("biography", None)
        user = User.objects.create_user(**validated_data)
        if school_name:
            user.teacherprofile.school_name = school_name
        if biography:
            user.teacherprofile.biography = biography
        user.teacherprofile.save()
        return user


class ActivationResendApiSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "user does not exist"})
        if user_object.is_verified:
            raise serializers.ValidationError(
                {"message": "user is already activated and verified"}
            )
        attrs["user"] = user_object
        return super().validate(attrs)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False, write_only=True
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.", code="authorization"
                )
            if not user.is_verified:
                raise serializers.ValidationError("user is not verified")
        else:
            raise serializers.ValidationError(
                "Must include email and password.", code="authorization"
            )

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError("user is not verified")
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.id
        return validate_data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"detail": "passwords must match"})
        try:
            validate_password(attrs.get("new_password1"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password1": list(e.messages)})
        return super().validate(attrs)
