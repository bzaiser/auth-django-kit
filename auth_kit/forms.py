from django import forms
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label=_("E-Mail"), required=False)
    first_name = forms.CharField(label=_("Vorname"), max_length=150, required=False)
    last_name = forms.CharField(label=_("Nachname"), max_length=150, required=False)

    class Meta:
        model = UserProfile
        fields = [
            "display_name",
            "phone",
            "timezone",
            "language",
            "avatar",
            "avatar_color",
            "bio",
            "notify_email",
        ]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*", "class": "form-control form-control-sm"}),
            "avatar_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"}),
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.fields["email"].initial = user.email
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif name != "avatar_color":
                field.widget.attrs.setdefault("class", "form-control")

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user is not None and commit:
            self.user.email = self.cleaned_data.get("email", "")
            self.user.first_name = self.cleaned_data.get("first_name", "")
            self.user.last_name = self.cleaned_data.get("last_name", "")
            self.user.save(update_fields=["email", "first_name", "last_name"])
        if commit:
            profile.save()
        return profile
