import os
import sys

import django
from django.conf import settings
from django.core.management import call_command
from django.test import Client, TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS_DIR = os.path.join(os.path.dirname(BASE_DIR), "django-design-studio")
for p in (BASE_DIR, DS_DIR):
    if p not in sys.path and os.path.isdir(p):
        sys.path.insert(0, p)

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="test-auth-kit",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "design_studio",
            "auth_kit",
        ],
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],
        ROOT_URLCONF="tests.test_auth_kit",
        TEMPLATES=[{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "design_studio.context_processors.theme_context",
                ],
            },
        }],
        STATIC_URL="/static/",
        LOGIN_URL="auth_kit:login",
        LOGIN_REDIRECT_URL="/accounts/profile/",
    )
    django.setup()

from django.contrib.auth import get_user_model
from django.urls import include, path

urlpatterns = [
    path("design-studio/", include("design_studio.urls")),
    path("accounts/", include("auth_kit.urls")),
]


class AuthKitTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="alice", password="pw", email="a@example.com")
        self.client = Client()

    def test_login_profile_update_and_token_generation(self):
        login_page = self.client.get("/accounts/login/")
        self.assertEqual(login_page.status_code, 200)

        self.client.force_login(self.user)
        prof_page = self.client.get("/accounts/profile/")
        self.assertEqual(prof_page.status_code, 200)

        resp = self.client.post(
            "/accounts/profile/",
            {
                "display_name": "Alice Admin",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Admin",
                "phone": "+49 123",
                "timezone": "Europe/Berlin",
                "language": "de",
                "avatar_color": "#6610f2",
                "bio": "NAS Admin",
                "notify_email": "on",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "alice@example.com")
        self.assertEqual(self.user.auth_kit_profile.display_name, "Alice Admin")
        self.assertEqual(self.user.auth_kit_profile.initials, "AA")

        tok_resp = self.client.post("/accounts/profile/token/")
        self.assertEqual(tok_resp.status_code, 302)
        self.user.auth_kit_profile.refresh_from_db()
        self.assertEqual(len(self.user.auth_kit_profile.api_token), 48)


if __name__ == "__main__":
    from django.test.runner import DiscoverRunner
    call_command("migrate", verbosity=0)
    runner = DiscoverRunner(verbosity=2)
    sys.exit(bool(runner.run_tests(["tests.test_auth_kit"])))
