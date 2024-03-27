from .models import Exercise
from .permissions import IsTeacherOrReadOnly
from rest_framework.views import APIView
from .serilizers import NewsSerializer


class NewAPIView(APIView):
    queryset = Exercise.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsTeacherOrReadOnly,]
