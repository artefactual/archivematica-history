from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SuperUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
