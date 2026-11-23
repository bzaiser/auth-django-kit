from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
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
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Benutzerprofil gespeichert."))
            return redirect("auth_kit:profile")
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    ctx = {"form": form, "profile": profile}
    app_tpl = (getattr(django_settings, "AUTH_KIT_APP_TAB_TEMPLATE", "") or "").strip() or "auth_kit/app_settings_tab.html"
    try:
        get_template(app_tpl)
        ctx["app_tab_template"] = app_tpl
        ctx["app_tab_label"] = getattr(django_settings, "AUTH_KIT_APP_TAB_LABEL", _("App-Einstellungen"))
        ctx["app_tab_icon"] = getattr(django_settings, "AUTH_KIT_APP_TAB_ICON", "bi-sliders")
        extra_ctx_fn = getattr(django_settings, "AUTH_KIT_APP_TAB_CONTEXT", None)
        if isinstance(extra_ctx_fn, str) and extra_ctx_fn.strip():
            extra_ctx_fn = import_string(extra_ctx_fn.strip())
        if callable(extra_ctx_fn):
            extra = extra_ctx_fn(request)
            if isinstance(extra, dict):
                ctx.update(extra)
    except TemplateDoesNotExist:
        pass
    if request.user.is_staff:
        try:
            from ops_kit.views import get_updates_context
            ctx.update(get_updates_context())
        except Exception:
            pass
    return render(request, "auth_kit/profile.html", ctx)


@login_required
@require_POST
def regenerate_token_view(request):
    profile = UserProfile.for_user(request.user)
    profile.regenerate_token()
    messages.success(request, _("Neuer API-Token generiert."))
    return redirect("auth_kit:profile")
