from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .forms import UserProfileForm
from .models import UserProfile


class StudioLoginView(LoginView):
    template_name = "auth_kit/login.html"
    redirect_authenticated_user = True


class StudioLogoutView(LogoutView):
    next_page = reverse_lazy("auth_kit:login")


class StudioPasswordChangeView(PasswordChangeView):
    template_name = "auth_kit/password_change.html"
    success_url = reverse_lazy("auth_kit:profile")

    def form_valid(self, form):
        messages.success(self.request, _("Passwort erfolgreich geändert."))
        return super().form_valid(form)


@login_required
def profile_view(request):
    profile = UserProfile.for_user(request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Benutzerprofil gespeichert."))
            return redirect("auth_kit:profile")
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(
        request,
        "auth_kit/profile.html",
        {"form": form, "profile": profile},
    )


@login_required
@require_POST
def regenerate_token_view(request):
    profile = UserProfile.for_user(request.user)
    profile.regenerate_token()
    messages.success(request, _("Neuer API-Token generiert."))
    return redirect("auth_kit:profile")
