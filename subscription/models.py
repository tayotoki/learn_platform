from django.db import models


class CourseSubscription(models.Model):
    """
    Подписка пользователя на курс
    """

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    is_active = models.BooleanField(default=False, verbose_name="Подписка активна")
    active_since = models.DateField(verbose_name="От", null=True)

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курс"

    def __str__(self):
        return f"{self.course} - {self.user}"
