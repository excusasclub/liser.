# lists/forms.py
from django import forms
from .models import BagList, ListVisibility

class BagListForm(forms.ModelForm):
    class Meta:
        model = BagList
        fields = [
            "title",
            "description",
            "visibility",
            "cover_image_url",
            "allow_forks",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input w-full rounded-lg border-gray-300",
                "placeholder": "Nombre de tu lista"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-textarea w-full rounded-lg border-gray-300",
                "rows": 3,
                "placeholder": "Descripción breve de la lista"
            }),
            "visibility": forms.Select(attrs={
                "class": "form-select w-full rounded-lg border-gray-300"
            }),
            "cover_image_url": forms.URLInput(attrs={
                "class": "form-input w-full rounded-lg border-gray-300",
                "placeholder": "URL de la imagen de portada (opcional)"
            }),
            "allow_forks": forms.CheckboxInput(attrs={
                "class": "form-checkbox h-5 w-5 text-green-600"
            }),
        }
