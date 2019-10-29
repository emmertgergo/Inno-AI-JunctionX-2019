from django import forms
from django.utils.safestring import mark_safe


class ReportPicture(forms.Form):
    image = forms.ImageField()

    def clean(self):
        super().clean()