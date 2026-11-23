import secrets

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auth_kit_profile",
    )
    display_name = models.CharField(max_length=80, blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    timezone = models.CharField(max_length=64, blank=True, default="Europe/Berlin")
    language = models.CharField(max_length=16, blank=True, default="de")
    bio = models.TextField(blank=True, default="")
    avatar = models.FileField(upload_to="auth_kit/avatars/", blank=True, null=True)
    avatar_color = models.CharField(max_length=16, blank=True, default="#0d6efd")
    notify_email = models.BooleanField(default=True)
    api_token = models.CharField(max_length=64, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def for_user(cls, user):
        profile, _ = cls.objects.get_or_create(user=user)
        return profile

    def regenerate_token(self) -> str:
        self.api_token = secrets.token_hex(24)
        self.save(update_fields=["api_token", "updated_at"])
        return self.api_token

    @property
    def initials(self) -> str:
        name = (self.display_name or self.user.get_full_name() or self.user.username or "U").strip()
        parts = [p[0].upper() for p in name.split() if p]
        return "".join(parts[:2]) or "U"

    def __str__(self):
        return f"Profile({self.user})"
