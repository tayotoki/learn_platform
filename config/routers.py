from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from courses.views import CourseViewSet
from users.views import UserProfileViewSet
from payment.views import PaymentViewSet

if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"users", UserProfileViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")
