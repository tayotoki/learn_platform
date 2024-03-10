from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet, Exists, OuterRef, Count


from subscription.models import CourseSubscription
from users.models import User


class CourseQuerySet(QuerySet):
    def annotate_subscribe(self, user: User | AnonymousUser) -> "QuerySet":
        return self.annotate(
            is_subscribed=Exists(
                CourseSubscription.objects.filter(
                    course_id=OuterRef("pk"),
                    user=user,
                    is_active=True
                )
            )
        )

    def annotate_lessons_count(self) -> "QuerySet":
        return self.annotate(
            lessons_count=Count("lessons")
        )
