from .models import New
from .permissions import IsTeacherOrReadOnly
from rest_framework.views import APIView
from .serilizers import NewsSerializer


class NewAPIView(APIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsTeacherOrReadOnly,]