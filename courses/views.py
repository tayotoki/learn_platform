from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Course, Lesson
from .serializers import (
    CourseRetrieveSerializer,
    CourseSerializer,
    LessonListSerializer,
    LessonRetrieveSerializer,
)
from .filters import BaseCourseFilter


# @extend_schema(tags="Courses")
class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    filterset_class = BaseCourseFilter

    def get_queryset(self):
        queryset = Course.objects.all().select_related("author")

        if self.action == self.retrieve.__name__:
            queryset = queryset.prefetch_related("lessons")

        return queryset

    def get_serializer_class(self):
        serializer_class = CourseSerializer

        if self.action == self.retrieve.__name__:
            serializer_class = CourseRetrieveSerializer

        return serializer_class


class LessonAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    pagination_class = LimitOffsetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course',
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.NUMBER,
                description='ID курса для фильтрации уроков',
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Lesson.objects.all().select_related("course")

        course_id = self.request.query_params.get("course")
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related("course")
    serializer_class = LessonRetrieveSerializer
