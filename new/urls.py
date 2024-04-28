from new.views import ListNewAPIView, CreateNewAPIView, EditNews
from django.urls import path

app_name = "new"

urlpatterns = [
    path('list/', ListNewAPIView.as_view(), name='news-list-create'),
    path('create/', CreateNewAPIView.as_view(), name='news-create'),
    path('edit-news/<int:pk>/', EditNews.as_view(), name='edit-news'),
]
