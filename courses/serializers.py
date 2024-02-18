from rest_framework import serializers

from .models import Course, Lesson


class LessonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CoursePaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_type(self, obj) -> str:
        return obj._meta.model.__name__.lower()


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
