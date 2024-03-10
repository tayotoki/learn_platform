from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "content_type", "type", "is_confirmed")
    readonly_fields = ("is_confirmed",)

    def __getattribute__(self, item):
        match item:
            case (
                "has_add_permission" |
                "has_delete_permission" |
                "has_change_permission"
            ):
                return lambda request, obj=None: False
        return super().__getattribute__(item)
