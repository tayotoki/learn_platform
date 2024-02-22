from django.db import models
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from courses.models import Course


class BaseCourseFilter(FilterSet):
    name = CharFilter(method="filter_name", label="Фильтр по названиями курсов или уроков в курсах")

    class Meta:
        model = Course
        fields = ()

    @staticmethod
    def filter_name(queryset, _, value):
        return queryset.filter(
            models.Q(name__icontains=value) | models.Q(lessons__name__icontains=value)
        ).distinct()
