from rest_framework import serializers
from .models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    imagen = serializers.ImageField(required=False, allow_null=True)
    analisis_ia = serializers.CharField(read_only=True, required=False)
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'stock', 'precio', 'categoria', 'categoria_nombre', "imagen", 'analisis_ia']
        read_only_fields = ['id', 'categoria_nombre', 'analisis_ia']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']