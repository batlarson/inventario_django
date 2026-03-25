from django.contrib import admin
from .models import Producto, Categoria, Historial, Perfil

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Historial)
admin.site.register(Perfil)