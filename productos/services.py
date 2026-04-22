from django.core.exceptions import ValidationError
from .models import Producto

class ProductoService:
   
    @staticmethod
    def vender_producto(producto_id, cantidad_vendida=1):
        producto = Producto.objects.get(pk=producto_id)
        
        # Lógica de negocio: No vendemos si no hay stock
        if producto.stock < cantidad_vendida:
            raise ValidationError(f"No hay suficiente stock para {producto.nombre}")
        
        producto.stock -= cantidad_vendida
        producto.save()
        
        return producto