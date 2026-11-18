# auth-django-kit

Wiederverwendbares Auth- & Benutzerprofil-Paket für Django + `django-design-studio`.

## Features
- Login / Logout / Passwort ändern im `django-design-studio`-Look (ohne CDN)
- Vollständiges Benutzerprofil (`UserProfile`): Anzeigename, E-Mail, Telefon, Zeitzone, Sprache, Bio, Avatar-Farbe, API-Token-Generierung, E-Mail-Benachrichtigungs-Opt-In
- Direktlink ins Design Studio (`design_studio:studio`)

## Installation
```bash
pip install --no-user --upgrade --no-cache-dir git+https://github.com/bzaiser/auth-django-kit.git@main
```

```python
# settings.py
INSTALLED_APPS = [..., "design_studio", "auth_kit"]
LOGIN_URL = "auth_kit:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "auth_kit:login"

# urls.py
path("accounts/", include("auth_kit.urls")),
```
