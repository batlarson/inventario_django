from django import forms
from .models import Producto
import re

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'precio', 'perecedero', 'categoria', 'imagen']
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("¡El precio debe ser mayor que cero! No estamos regalando nada.")
        return precio
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if len(nombre) < 3:
            raise forms.ValidationError("El nombre es demasiado corto, pon algo más descriptivo.")
        
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras, números y espacios. ¡Nada de símbolos extraños!")
        
        return nombre