from rest_framework import serializers
from .models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    imagen = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'stock', 'precio', 'categoria', 'categoria_nombre', "imagen"]

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']