from rest_framework import serializers
from .models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'stock', 'precio', 'categoria', 'categoria_nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']