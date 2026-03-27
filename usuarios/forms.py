from django import forms
from .models import Perfil
import re

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar']