import os
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import URL
from .services import generate_short_url


class UserURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = [
            "id",
            "orig_url",
            "shorted_url"]


class UserSerializer(serializers.ModelSerializer):
    urls = UserURLSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_active",
            "urls"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        validated_data["is_active"] = validated_data.get("is_active", False)
        validated_data["is_superuser"] = validated_data.get(
            "is_superuser", False)

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance


class URLUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "last_name",
            "first_name"
        ]


class URLSerializer(serializers.ModelSerializer):
    user = URLUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = URL
        fields = [
            "id",
            "orig_url",
            "shorted_url",
            "click_stat",
            "created_at",
            "user"
        ]
        read_only_fields = ["shorted_url", "click_stat"]

    def get_host_url(self) -> str | None:
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri("/")

    def create(self, validated_data: dict) -> URL:
        length = int(os.getenv("SHORT_URL_LENGHT"))
        short_url = self.get_host_url() + generate_short_url(length)

        while URL.objects.filter(shorted_url=short_url).exists():
            short_url = self.get_host_url() + generate_short_url(length)
            length += 1

        validated_data["shorted_url"] = short_url
        url = URL(**validated_data)
        url.save()

        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user = self.context['request'].user

        if not user.is_superuser:
            representation.pop('click_stat', None)
            representation.pop('user', None)

        return representation
