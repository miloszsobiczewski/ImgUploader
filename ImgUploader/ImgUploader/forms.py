from django import forms
from . import models


class ImageForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=[(x, x) for x in ['Google Drive', 'local']], required=True)
    size = forms.ChoiceField(
        choices=[(x, x) for x in ['800x600', '480x640']], required=True)

    class Meta:
        model = models.Image
        fields = ['type', 'size', 'picture']



