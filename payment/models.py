from django.contrib.contenttypes.fields import GenericForeignKey
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
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    amount = models.DecimalField(verbose_name="Сумма оплаты", max_digits=6, decimal_places=2)
    type = models.CharField(verbose_name="Способ оплаты", choices=PaymentType.choices)
