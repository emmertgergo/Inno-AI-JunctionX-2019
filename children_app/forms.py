from django import forms
from .models import Child


class AddChild(forms.ModelForm):

    class Meta:
        model = Child
        fields = ('name', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),

        }
        labels = {
                'name': "Name of the family member:",
        }

    def clean(self):
        all_clean_data = super().clean()


class SettingsEmoji(forms.ModelForm):

    class Meta:
        model = Child
        fields = ('emojitype',)
        widgets = {
            'emojitype': forms.NumberInput(attrs={'min': '1', 'max': '2'}),

        }
        labels = {
                'emojitype': "Type of the emoji: ",
        }

    def clean(self):
        all_clean_data = super().clean()
