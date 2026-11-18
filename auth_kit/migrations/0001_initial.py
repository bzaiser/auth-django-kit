from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("display_name", models.CharField(blank=True, default="", max_length=80)),
                ("phone", models.CharField(blank=True, default="", max_length=40)),
                ("timezone", models.CharField(blank=True, default="Europe/Berlin", max_length=64)),
                ("language", models.CharField(blank=True, default="de", max_length=16)),
                ("bio", models.TextField(blank=True, default="")),
                ("avatar_color", models.CharField(blank=True, default="#0d6efd", max_length=16)),
                ("notify_email", models.BooleanField(default=True)),
                ("api_token", models.CharField(blank=True, default="", max_length=64)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_kit_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
