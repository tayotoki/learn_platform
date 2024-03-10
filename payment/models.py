from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from users.models import User
from .constants import PaymentType


class Payment(PolymorphicModel):
    """
    Оплата
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateField(verbose_name="Дата оплаты", auto_now_add=True)
    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный продукт",
        limit_choices_to={"app_label": "courses"},
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    amount = models.DecimalField(
        verbose_name="Сумма оплаты",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    type = models.CharField(verbose_name="Способ оплаты", choices=PaymentType.choices)
    is_confirmed = models.BooleanField(verbose_name="Подтвержден", default=False)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.amount}"
