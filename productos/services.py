from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
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
    
    @staticmethod
    def aplicar_inflacion_masiva(porcentaje=10):
        """
        Aumenta el precio de todos los productos usando una sola query SQL (protegido por transaction).
        """
        factor = 1 + (porcentaje / 100.0) # Si es 10, el factor es 1.10

        try:
            with transaction.atomic():        
                # Procesamiento masivo con F()    Como uso transaction deberia ser "Todo o Nada"
                filas_actualizadas = Producto.objects.update(precio=F('precio') * factor)
            return filas_actualizadas
        except Exception as e:
            raise Exception(f"Fallo masivo. Se ha cancelado la operación: {e}")