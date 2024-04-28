from exercise.views import ListExerciseAPIView, CreateExerciseAPIView, EditExercise
from django.urls import path

app_name = "exercise"

urlpatterns = [
    path('list/', ListExerciseAPIView.as_view(), name='exercise-list'),
    path('create/', CreateExerciseAPIView.as_view(), name='exercise-create'),
    path('edit-news/<int:pk>/', EditExercise.as_view(), name='edit-news'),
]


