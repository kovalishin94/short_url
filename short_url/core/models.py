from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    orig_url = models.URLField()
    shorted_url = models.URLField(unique=True)
    click_stat = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="urls")

    class Meta:
        ordering = ["created_at"]
