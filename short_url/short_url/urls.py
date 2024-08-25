from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.api import redirect_to_origin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
    path("api/", include("core.urls")),
    path("<str:short_url>/", redirect_to_origin, name="redirect_to_origin")
]
