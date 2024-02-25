from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Course, Lesson
from .serializers_mixins import ProductTypeMixin
from .validators import YouTubeLinkValidator


class LessonRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['author']


class LessonCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания нового урока с проверкой, что пользователель
    автор курса и ссылка для урока из youtube
    """

    video_link = serializers.URLField(validators=[YouTubeLinkValidator()])

    class Meta:
        model = Lesson
        exclude = ("author",)

    def validate_course(self, data):
        course_name = data

        course = get_object_or_404(Course, name=course_name)

        if course.author != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to add lesson to this course")

        return course_name


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

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CourseRetrieveSerializer(CourseSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = CourseSerializer.Meta.fields + ("lessons", "is_subscribed", "lessons_count")
