from .models import New
from rest_framework.generics import ListAPIView,CreateAPIView, RetrieveUpdateAPIView
from .serilizers import NewsSerializer
from account.permissions import IsAdminOrStudent, IsAdminOrTeacher


class ListNewAPIView(ListAPIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrTeacher]


class CreateNewAPIView(CreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrTeacher]


class EditNews(RetrieveUpdateAPIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)