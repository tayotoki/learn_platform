from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwnerOrManager
from .filters import BaseCourseFilter
from .models import Lesson
from .serializers import (
    CourseRetrieveSerializer,
    CourseSerializer,
    LessonListSerializer,
    LessonRetrieveSerializer,
)
from .viewsets_mixins import UserLimitedOrManagerAllMixin


@extend_schema(tags=["Courses"])
class CourseViewSet(UserLimitedOrManagerAllMixin, viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    filterset_class = BaseCourseFilter
    permission_classes = [IsOwnerOrManager]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == self.retrieve.__name__:
            queryset = queryset.prefetch_related("lessons")

        return queryset

    def get_serializer_class(self):
        serializer_class = CourseSerializer

        if self.action == self.retrieve.__name__:
            serializer_class = CourseRetrieveSerializer

        return serializer_class


@extend_schema(tags=["Lessons"])
class LessonAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

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


@extend_schema(tags=["Lessons"])
class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related("course")
    serializer_class = LessonRetrieveSerializer
    permission_classes = [IsOwnerOrManager]
