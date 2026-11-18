from django.urls import path

from . import views

app_name = "auth_kit"

urlpatterns = [
    path("login/", views.StudioLoginView.as_view(), name="login"),
    path("logout/", views.StudioLogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/token/", views.regenerate_token_view, name="regenerate_token"),
    path("password/", views.StudioPasswordChangeView.as_view(), name="password_change"),
]
