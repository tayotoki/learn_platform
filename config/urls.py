from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .routers import router

from courses.views import LessonAPIView, LessonDetailAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/lessons/", LessonAPIView.as_view(), name="lessons-list"),
    path("api/lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lessons-detail"),
]

if settings.API_DOCS_ENABLE:
    urlpatterns += (
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
    )
