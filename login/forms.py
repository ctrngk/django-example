########################################
# login/forms.py
########################################


from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput,
                                label=_("Username"),
                                error_messages={'invalid': _(
                                    "This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(max_length=30, widget=forms.TextInput, label=_("Email address"))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput, label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
