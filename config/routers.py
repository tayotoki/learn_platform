from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from courses.views import CourseViewSet

if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r"courses", CourseViewSet, basename="courses")
