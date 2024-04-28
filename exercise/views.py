from rest_framework import status
from rest_framework.response import Response
from account.permissions import IsAdminOrStudent, IsAdminOrTeacher
from rest_framework.views import APIView
from exercise.serilizers import ExerciseSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .models import Exercise

# class NewAPIView(APIView):
#     queryset = Exercise.objects.all()
#     serializer_class = NewsSerializer
#     permission_classes = [IsTeacherOrReadOnly,]


# class CreateAssignment(APIView):
#     permission_classes = [IsAdminOrTeacher]
#
#     def post(self, request):
#         serializer = ExerciseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListExerciseAPIView(ListAPIView):
    permission_classes = [IsAdminOrTeacher]
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class CreateExerciseAPIView(CreateAPIView):
    permission_classes = [IsAdminOrTeacher]
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class EditExercise(RetrieveUpdateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdminOrTeacher]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)