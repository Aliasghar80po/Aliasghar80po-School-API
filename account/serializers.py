from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User, Teacher, Student, Course
from exercise.models import Exercise
from django.utils import timezone
from datetime import timedelta
from rest_framework.fields import DictField
from new.models import New
import os
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    national_code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Teacher
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'national_code',
                  'school_name', 'biography']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        errors = {}
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        if Teacher.objects.filter(username=attrs['username']).exists():
            errors['username'] = ['Username already exists']
        if errors:
            raise ValidationError(DictField().to_internal_value(errors))
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = Teacher.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TeacherUpdateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    national_code = serializers.CharField(required=False)

    class Meta:
        model = Teacher
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'national_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class StudentUpdateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    national_code = serializers.CharField(required=False)

    class Meta:
        model = Teacher
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'national_code']
        extra_kwargs = {'password': {'write_only': True}}


class StudentRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    national_code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Student
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'national_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password2')
        first_name = validated_data.get('first_name')
        user = Student.objects.create(**validated_data)
        user.set_password(password)
        user.username = first_name
        user.save()
        return user


class StudentLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=30, required=True)
    national_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'national_code']


class TeacherLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=30, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'national_code']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'national_code']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return attrs


class AddStudentSerializer(serializers.ModelSerializer):
    national_code = serializers.CharField(max_length=10, required=True)
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)

    class Meta:
        model = Student
        fields = ['national_code', 'teacher']

    def validate_teacher(self, value):
        # در اینجا معلم مرتبط با کاربر جاری (با توکن) شناسایی می‌شود
        user = self.context['request'].user
        teacher = user.teacher
        if teacher is not None:
            return teacher
        else:
            raise serializers.ValidationError("The user is not a teacher.")


class AddNewSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)

    class Meta:
        model = New
        fields = ['title', 'body', 'teacher']

    def validate_teacher(self, value):
        # در اینجا معلم مرتبط با کاربر جاری (با توکن) شناسایی می‌شود
        user = self.context['request'].user
        teacher = user.teacher
        if teacher is not None:
            return teacher
        else:
            raise serializers.ValidationError("The user is not a teacher.")


class NewUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=True)

    class Meta:
        model = New
        fields = ['title', 'body', 'teacher']


class AddExerciseSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)
    deadline = serializers.DateTimeField(required=True)
    attached_file = serializers.FileField(allow_empty_file=True, required=False)

    class Meta:
        model = Exercise
        fields = ['teacher', 'title', 'body', 'deadline', 'attached_file']  # Include the 'teacher' field here

    def validate_teacher(self, value):
        # در اینجا معلم مرتبط با کاربر جاری (با توکن) شناسایی می‌شود
        user = self.context['request'].user
        teacher = user.teacher
        if teacher is not None:
            return teacher
        else:
            raise serializers.ValidationError("The user is not a teacher.")

    def validate_deadline(self, value):
        if value < timezone.now() + timedelta(days=4):
            raise serializers.ValidationError("Deadline must be at least four days from now.")
        return value

    def validate_attached_file(self, value):

        if value:
            # Get the file extension
            ext = os.path.splitext(value.name)[1]
            # Check if the file extension is allowed
            if not ext.lower() in ['.pdf', '.zip']:
                raise ValidationError("Only PDF or ZIP files are allowed.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), required=True)

    class Meta:
        model = Course
        fields = ['teacher', 'name', 'description', 'teacher', 'student']

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=254)
#
#     class Meta:
#         fields = ['email']  # Define the fields used by the serializer
#
#     def validate(self, attrs):
#         """
#         Validate email and send password reset email to the user
#         """
#         email = attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             # Encode the user ID in URL-safe format
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             print('Encoded UID', uid)
#             # Generate a password reset token
#             token = PasswordResetTokenGenerator().make_token(user)
#             print('PasswordResetToken', token)
#             # Generate the password reset link
#             link = 'http://127.0.0.1:8000/api/user/reset/' + uid + '/' + token
#             print('Password reset link', link)
#             # Send the email
#             body = 'Click Following link to reset your password'+ link
#             data = {
#                 'subject': 'Password Reset Email',
#                 'body': body,
#                 'to_email': user.email,
#             }
#             Util.send_mail(data)
#             return attrs
#         else:
#             raise ValidationError("You are not a registered user")
#
#
# class UserResetPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('password', 'password2')  # Define the fields used by the serializer
#
#     def validate(self, attrs):
#         """
#         Validate and reset the user's password
#         """
#         try:
#             password = attrs.get('password')
#             password2 = attrs.get('password2')
#             uid = self.context.get('uid')
#             token = self.context.get('token')
#             if password != password2:
#                 raise serializers.ValidationError("Passwords do not match")
#             # Decode the user ID from URL-safe format
#             id = smart_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(id=id)
#             # Check the token validity
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise ValidationError("Token is not valid or has expired")
#             # Change the password and save the user
#             user.set_password(password)
#             user.save()
#             return attrs
#         except DjangoUnicodeDecodeError as identifier:
#             PasswordResetTokenGenerator().make_token(user, token)
#             raise ValidationError("Token is not valid or has expired")
