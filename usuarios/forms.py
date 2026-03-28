from django import forms
from .models import Perfil
from django.core.exceptions import ValidationError
import re

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar', 'telefono']
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'mi-clase-css', 
                'placeholder': 'Ej: +34 600 000 000',
                'style': 'border: 2px solid #4CAF50; border-radius: 5px; padding: 10px;'
            }),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            limite_mb = 2
            if avatar.size > limite_mb * 1024 * 1024:
                raise ValidationError(f"La imagen es demasiado grande. El límite es de {limite_mb}MB.")
        
        return avatar