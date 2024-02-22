from .models import Course


class UserLimitedOrManagerAllMixin:
    """
    Миксин для фильтрации кверисета по пользователю,
    если запрос выполнил пользователь.
    Если запрос выполнил менеджер - кверисет без фильтра.
    """
    def get_queryset(self):
        queryset = (
            Course.objects
            .select_related("author")
        )

        if self.action == self.list.__name__:
            if not self.request.user.groups.filter(name='managers').exists():
                queryset = queryset.filter(author=self.request.user)

            return queryset
