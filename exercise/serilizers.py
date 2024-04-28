from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import Student, Teacher
from .models import Exercise, ExerciseResponse
import os


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseResponseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), required=False)
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)

    class Meta:
        model = ExerciseResponse
        fields = ("student", "teacher", "response_text", "attached_file", "id")

    def validate_attached_file(self, value):

        if value:
            # Get the file extension
            ext = os.path.splitext(value.name)[1]
            # Check if the file extension is allowed
            if not ext.lower() in ['.pdf', '.zip']:
                raise ValidationError("Only PDF or ZIP files are allowed.")
        return value
