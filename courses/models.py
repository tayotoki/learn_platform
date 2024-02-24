from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from courses.querysets import CourseQuerySet
from payment.models import Payment
from users.models import User


class Course(models.Model):
    name = models.CharField(verbose_name="Название", max_length=64)
    preview = models.ImageField(verbose_name="Превью", upload_to='courses/previews', null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.SET_NULL, related_name='courses', null=True
    )
    payments = GenericRelation(Payment, object_id_field="course_object_id")

    objects = CourseQuerySet.as_manager()

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    name = models.CharField(verbose_name="Название", max_length=64)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    preview = models.ImageField(verbose_name="Превью", upload_to='lessons/previews', null=True, blank=True)
    video_link = models.URLField(verbose_name="Ссылка на видео", null=True, blank=True)
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.CASCADE, related_name='lessons'
    )
    payments = GenericRelation(Payment, object_id_field="lesson_object_id")
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.SET_NULL, related_name='lessons', null=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name}"
