from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("users/", include("users.urls", namespace="users")),
    path("api/lessons/", include("courses.urls", namespace="courses")),
    path('payment_update/', include("payment.urls", namespace="payment")),
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
