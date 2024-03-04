from django.db.models import Prefetch, OuterRef, QuerySet
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import viewsets, generics, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscription.models import CourseSubscription
from users.permissions import IsOwnerOrManager
from .filters import BaseCourseFilter
from .models import Lesson, Course
from .querysets import CourseQuerySet
from .serializers import (
    CourseRetrieveSerializer,
    CourseSerializer,
    LessonListSerializer,
    LessonRetrieveSerializer,
    LessonCreateSerializer,
)
from .viewsets_mixins import UserLimitedOrManagerAllMixin
from .pagination import CourseLessonPagination


@extend_schema(tags=["Courses"])
class CourseViewSet(UserLimitedOrManagerAllMixin, viewsets.ModelViewSet):
    pagination_class = CourseLessonPagination
    filterset_class = BaseCourseFilter
    permission_classes = [IsOwnerOrManager]

    @extend_schema(
        tags=["Courses"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Подписка оформлена успешно",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="У вас уже есть активная подписка на этот курс",
            ),
        },
        request=None,
    )
    @action(detail=True, methods=["POST"], url_path="subscribe")
    def subscribe(self, request, *args, **kwargs) -> Response:
        """
        Оформление подписки на курс, можно отправлять пустой request_body
        """

        course = self.get_object()
        user = request.user

        subscription, is_created = CourseSubscription.objects.get_or_create(
            course=course, user=user, is_active=True
        )

        if is_created:
            subscription.active_since = timezone.now()
            subscription.save(update_fields=["active_since"])
            
            return Response(
                {"message": "Вы успешно подписались на курс."}, status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "У вас уже есть активная подписка на этот курс."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        tags=["Courses"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Подписка отменена",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Отсутствует активная подписка на данный курс",
            ),
        },
        request=None,
    )
    @action(detail=True, methods=["DELETE"], url_path="unsubscribe")
    def unsubscribe(self, request, *args, **kwargs) -> Response:
        """
        Отмена подписки на курс
        """

        subscription = (
            CourseSubscription.objects
            .filter(
                course=self.get_object(),
                user=request.user,
                is_active=True
            )
            .select_related("user", "course")
        )

        status_code = status.HTTP_400_BAD_REQUEST

        if subscription.exists():
            subscription.delete()
            status_code = status.HTTP_204_NO_CONTENT

        return Response(status=status_code)

    def get_queryset(self):
        queryset: QuerySet[Course] = super().get_queryset()

        if self.action == self.retrieve.__name__:  # noqa
            queryset: CourseQuerySet = (
                queryset.prefetch_related(
                    "lessons",
                    Prefetch(
                        "subscriptions",
                        queryset=CourseSubscription.objects.filter(course_id=self.kwargs["pk"]),
                    ),
                )
                .annotate_subscribe(user_id=self.request.user.id)
                .annotate_lessons_count()
            )

        if self.action == self.list.__name__:  # noqa
            queryset: CourseQuerySet = (
                queryset
                .prefetch_related("lessons")
                .annotate_lessons_count()
            )

        return queryset

    def get_serializer_class(self):
        serializer_class = CourseSerializer

        if self.action == self.retrieve.__name__:
            serializer_class = CourseRetrieveSerializer

        return serializer_class


@extend_schema(tags=["Lessons"])
class LessonAPIView(generics.ListCreateAPIView):
    serializer_class = LessonListSerializer
    pagination_class = CourseLessonPagination
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
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Lesson.objects.all().select_related("course")

        course_id = self.request.query_params.get("course")
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset

    def get_serializer_class(self):
        self.action_ = self.request.method.lower()
        serializer_class = self.__class__.serializer_class

        match self.action_:
            case self.post.__name__:
                serializer_class = LessonCreateSerializer

        return serializer_class


@extend_schema(tags=["Lessons"])
class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related("course")
    serializer_class = LessonRetrieveSerializer
    permission_classes = [IsOwnerOrManager]
