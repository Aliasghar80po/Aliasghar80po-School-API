from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.serializers import TeacherRegistrationSerializer, StudentRegistrationSerializer, StudentLoginSerializer, \
    TeacherLoginSerializer, TeacherProfileSerializer, AddStudentSerializer, AddNewSerializer, AddExerciseSerializer, \
    TeacherUpdateSerializer, StudentUpdateSerializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminOrTeacher, IsStudent
from .models import Student, Teacher, Course
from new.models import New
from new.serilizers import NewsSerializer
from exercise.models import Exercise, ExerciseResponse
from exercise.serilizers import ExerciseSerializer, ExerciseResponseSerializer
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView
from django.utils.text import slugify
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class TeacherRegistrationAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = TeacherRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = TeacherLoginSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': {'non_field_errors': ['Email or Password is not valid']}}), status.HTTP_400_BAD_REQUEST


class TeacherUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherUpdateSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # Retrieve the teacher object associated with the current user
        return self.request.user.teacher


class TeacherLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            logout(request)
            return Response({'message': 'You have successfully logged out of your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No valid user found or you do not have permission.'},
                            status=status.HTTP_403_FORBIDDEN)


class TeacherProfileAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrTeacher]
    serializer_class = TeacherProfileSerializer

    def get(self, request, format=None):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentRegistrationAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = StudentLoginSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': {'non_field_errors': ['Email or Password is not valid']}}), status.HTTP_400_BAD_REQUEST


class StudentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # Retrieve the teacher object associated with the current user
        return self.request.user.student


class StudentLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'student'):
            logout(request)
            return Response({'message': 'You have successfully logged out of your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No valid user found or you do not have permission.'},
                            status=status.HTTP_403_FORBIDDEN)


class StudentProfileAPIView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, format=None):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddStudentToTeacher(GenericAPIView):
    serializer_class = AddStudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            national_code = serializer.validated_data.get('national_code')
            teacher = request.user.teacher
            if teacher is not None:
                try:
                    student = Student.objects.get(national_code=national_code)
                    teacher.students.add(student)

                    # Displaying courses taught by the teacher for the student
                    courses_taught_by_teacher = teacher.taught_courses.all()
                    for course in courses_taught_by_teacher:
                        student.enrolled_courses.add(course)

                    return Response({'message': 'Student added successfully'},
                                    status=status.HTTP_200_OK)
                except Student.DoesNotExist:
                    return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'User is not a teacher'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddNewToTeacher(GenericAPIView):
    serializer_class = AddNewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            teacher = request.user.teacher
            if teacher is not None:
                new_title = request.data.get('title')
                new_slug = slugify(new_title)  # converting title into slug
                try:
                    new = New.objects.get(slug=new_slug)
                except New.DoesNotExist:
                    new = New.objects.create(title=new_title, slug=new_slug)
                teacher.created_news.add(new)

                return Response({'message': 'خبر با موفقیت ایجاد شد'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'کاربر معلم نیست'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateNew(UpdateAPIView):
    serializer_class = AddNewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = request.user.teacher

        if teacher is not None:
            new_title = serializer.validated_data.get('title')
            new_slug = slugify(new_title)  # converting title into slug
            try:
                new = New.objects.get(slug=new_slug)
            except New.DoesNotExist:
                # If the new with the title doesn't exist, return an error
                return Response({'error': 'New not found'}, status=status.HTTP_404_NOT_FOUND)

            # No need to create or update the new, just associate it with the teacher
            teacher.created_news.add(new)
            return Response({'message': 'News updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not a teacher'}, status=status.HTTP_400_BAD_REQUEST)


class StudentNewList(ListAPIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        # Filtering teachers based on the current student
        teacher = Teacher.objects.filter(students=self.request.user.student)
        print(teacher)  # Print the teachers found (for debugging)

        # If at least one teacher is found, return exercises created by the first teacher
        if teacher is not None:
            return New.objects.filter(created_by=teacher[0])
        else:
            return New.objects.none()


class AddExerciseToTeacher(APIView):
    serializer_class = AddExerciseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            teacher = request.user.teacher
            if teacher is not None:
                new_title = request.data.get('title')
                try:
                    # Attempt to retrieve the exercise by title
                    exercise = Exercise.objects.get(title=new_title)
                except Exercise.DoesNotExist:
                    # If exercise with the title doesn't exist, create a new one
                    exercise = Exercise.objects.create(title=new_title)
                # Associate the exercise with the teacher
                teacher.created_exercise.add(exercise)
                return Response({'message': 'Exercise created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User is not a teacher'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateExercise(UpdateAPIView):
    serializer_class = AddExerciseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = request.user.teacher

        if teacher is not None:
            new_title = serializer.validated_data.get('title')
            try:
                # Attempt to retrieve the exercise by title
                exercise = Exercise.objects.get(title=new_title)
            except Exercise.DoesNotExist:
                # If exercise with the title doesn't exist, return an error
                return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

            # No need to create or update the exercise, just associate it with the teacher
            teacher.created_exercise.add(exercise)
            return Response({'message': 'Exercise updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not a teacher'}, status=status.HTTP_400_BAD_REQUEST)


class StudentExerciseList(ListAPIView):
    # Queryset of all exercises
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer  # Serializer class for exercises
    permission_classes = [IsAuthenticated, IsStudent]  # Permissions required for this view

    def get_queryset(self):
        # Filtering teachers based on the current student
        teacher = Teacher.objects.filter(students=self.request.user.student)
        print(teacher)  # Print the teachers found (for debugging)

        # If at least one teacher is found, return exercises created by the first teacher
        if teacher is not None:
            return Exercise.objects.filter(created_by=teacher[0])
        else:
            return Exercise.objects.none()


class ExerciseResponseListCreate(ListCreateAPIView):
    queryset = ExerciseResponse.objects.all()
    serializer_class = ExerciseResponseSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = request.user.student
        teacher = Teacher.objects.filter(students=self.request.user.student)
        exercise_id = request.data.get('exercise_id')

        if exercise_id is not None:
            try:
                exercise = Exercise.objects.get(id=exercise_id)
            except Exercise.DoesNotExist:
                return Response("Exercise not found", status=status.HTTP_404_NOT_FOUND)

            # Check if the deadline has not passed
            if exercise.deadline is None or exercise.deadline > timezone.now():
                if student in exercise.created_by.students.all():
                    serializer.validated_data['exercise_id'] = exercise_id
                    serializer.save(student=student, created_by=teacher[0])
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response("You are not allowed to respond to this exercise", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response("The deadline for this exercise has passed", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("Exercise ID is missing", status=status.HTTP_400_BAD_REQUEST)


class ExerciseResponseUpdate(UpdateAPIView):
    queryset = ExerciseResponse.objects.all()
    serializer_class = ExerciseResponseSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the exercise deadline has not passed
        exercise = instance.exercise
        if exercise.deadline is None or exercise.deadline > timezone.now():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response("The deadline for this exercise has passed", status=status.HTTP_403_FORBIDDEN)

# class EditNewByTeacherAPIView(RetrieveUpdateAPIView):
#     queryset = New.objects.all()
#     serializer_class = NewUpdateSerializer
#     permission_classes = [IsAdminOrTeacher]
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)


# class UserChangePasswordAPIView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, format=None):
#         serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# class SendPasswordResetEmailAPIView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, format=None):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message': 'Password reset link sent successfully. Please check your Email'},
#                             status=status.HTTP_200_OK)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserResetPasswordView(APIView):
#     renderer_classes = [UserRenderer]
#
#     def post(self, request, uid, token, format=None):
#         serializer = UserResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message': 'Password reset Successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
