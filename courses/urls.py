from django.urls import path

from .views import LessonAPIView, LessonDetailAPIView
from .apps import CoursesConfig


app_name = CoursesConfig.name


urlpatterns = [
    path("", LessonAPIView.as_view(), name="lessons-list"),
    path("<int:pk>/", LessonDetailAPIView.as_view(), name="lessons-detail"),
]
