########################################
# pollsForm/forms.py
########################################

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ('question', 'votes',)

    def clean_choice_text(self):
        try:
            Choice.objects.get(pk=self.cleaned_data['choice_text'])
        except Choice.DoesNotExist:
            raise forms.ValidationError(_("You didn't select a choice"))
        return self.cleaned_data['choice_text']