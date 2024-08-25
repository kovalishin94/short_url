from django.urls import path
from rest_framework import routers
from .api import UserViewSet, URLViewSet, me

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"urls", URLViewSet, basename="url")

urlpatterns = [
    path("me/", me, name="me")
]

urlpatterns += router.urls
