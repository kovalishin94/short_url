from django.db.models import Q
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import permissions
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .serializers import UserSerializer, URLSerializer
from .models import URL
from .permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("urls").order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        search = self.request.GET.get("search")

        if search:
            return User.objects.prefetch_related("urls").filter(
                Q(last_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(username__icontains=search))

        return super().get_queryset()

    def destroy(self, request: HttpRequest, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance == request.user:
            return Response({"Message": "You can't delete yourself"}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class URLViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):

    queryset = URL.objects.select_related("user")
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        search = self.request.GET.get("search")

        if not user.is_superuser:
            queryset = queryset.filter(user=user)

        if search:
            queryset = queryset.filter(
                Q(orig_url__icontains=search) |
                Q(shorted_url__icontains=search) |
                Q(user__username__icontains=search))

        return queryset

    def perform_create(self, serializer: URLSerializer) -> None:
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def redirect_to_origin(request: HttpRequest, short_url: str) -> Response:
    short_url = request.build_absolute_uri("/") + short_url
    try:
        url = URL.objects.get(shorted_url=short_url)
    except:
        url = None

    if not url:
        return Response(status=status.HTTP_404_NOT_FOUND)

    url.click_stat += 1
    url.save()

    return Response(status=status.HTTP_302_FOUND, headers={"Location": url.orig_url})


@api_view(["GET"])
def me(request: HttpRequest):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
