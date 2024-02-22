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

    def create(self, validated_data):
        print(self.context.get("request").user)
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CourseRetrieveSerializer(CourseSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = CourseSerializer.Meta.fields + ("lessons",)
