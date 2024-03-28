import jwt
from account.utils import send_email_thread
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from mail_templated import EmailMessage
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterApiSerializer,
    TeacherRegisterApiSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    ActivationResendApiSerializer,
)
from .permissions import IsAdminOrStudent, IsSuperUser, IsAdminOrTeacher

User = get_user_model()


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterApiSerializer
    permission_classes = [IsAdminOrStudent]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            serializer.save()
            user_object = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_object)
            email_object = EmailMessage(
                template_name="send_email/activation_email.html",
                context={"token": token},
                from_email="admin@gmail.com",
                to=[email],
            )
            send_email_thread(email_object)
            return Response(data={"email": email}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class TeacherRegisterApiView(GenericAPIView):
    serializer_class = TeacherRegisterApiSerializer
    permission_classes = [IsAdminUser, IsAdminOrTeacher]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_activation_email(user)
            return Response(data={"email": user.email}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_activation_email(self, user):
        token = self.get_token_for_user(user)
        email_object = EmailMessage(
            template_name="send_email/activation_email.html",
            context={"token": token},
            from_email="admin@gmail.com",
            to=[user.email],
        )
        email_object.send()

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ActivationConfirmApiView(APIView):
    def get(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response(
                {"message": "Token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"message": "Token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_id = token.get("user_id")
        user_object = get_object_or_404(User, pk=user_id)
        if user_object.is_verified:
            return Response({"message": "your account has already been verified"})
        user_object.is_verified = True
        user_object.save()
        return Response(
            data={
                "message": "your account have been verified and activated successfully"
            }
        )


class ActivationResendApiView(GenericAPIView):
    serializer_class = ActivationResendApiSerializer

    def post(self, request):
        serializer = ActivationResendApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.validated_data["user"]
        token = self.get_token_for_user(user_object)
        email_object = EmailMessage(
            template_name="send_email/activation_email.html",
            context={"token": token},
            from_email="admin@gmail.com",
            to=[user_object.email],
        )
        send_email_thread(email_object)
        return Response(
            data={"message": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        # return str(refresh.access_token)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        context = {
            "token": token.key,
            "user_id": user.pk,
            "email": user.email,
        }
        return Response(context)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(GenericAPIView):
    model = User
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_object = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user_object.check_password(serializer.data.get("old_password")):
                return Response(
                    data={"old_password": "wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_object.set_password(serializer.data.get("new_password1"))
            user_object.save()
            return Response(
                data={"message": "successfully password changed"},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
