from django.db.models import QuerySet, Exists, OuterRef

from subscription.models import CourseSubscription


class CourseQuerySet(QuerySet):
    def annotate_subscribe(self, user_id: int) -> "QuerySet":
        return self.annotate(
            is_subscribed=Exists(
                CourseSubscription.objects.filter(
                    course_id=OuterRef("pk"),
                    user_id=user_id,
                    is_active=True
                )
            )
        )