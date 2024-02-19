from rest_framework import serializers

from .models import Course, Lesson
from .serializers_mixins import ProductTypeMixin


class LessonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(ProductTypeMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CoursePaymentSerializer(ProductTypeMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "preview",
            "author",
        )


class CourseRetrieveSerializer(CourseSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = CourseSerializer.Meta.fields + ("lessons",)
