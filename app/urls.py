from django.contrib import admin
from django.urls import path, include

from django.urls import path, re_path, include
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Health Center API",
        default_version="v1",
        description="API for medical appointments management."
    ),
    public=True
)

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="auth"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="auth_refresh"),
    path("admin/", admin.site.urls),
    path("professionals/", include("app.professionals.urls")),
    path("appointments/", include("app.appointments.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
