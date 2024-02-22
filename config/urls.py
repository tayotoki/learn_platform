from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from courses.views import LessonAPIView, LessonDetailAPIView
from .routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/lessons/", LessonAPIView.as_view(), name="lessons-list"),
    path("api/lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lessons-detail"),
    path("users/", include("users.urls", namespace="users")),
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
