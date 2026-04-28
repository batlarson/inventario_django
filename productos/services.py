from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum, F
from .models import Producto, Historial
from .tasks import avisar_admin_sin_stock

import requests
import logging


class DashboardService:
    @staticmethod
    def obtener_estadisticas_usuario(usuario, moneda='EUR'):

        mis_productos = Producto.objects.filter(usuario=usuario)
        
        total_articulos = mis_productos.count()
        alertas = mis_productos.filter(stock__lt=10).count()
        recientes = Historial.objects.all().order_by('-fecha')[:5]

        resultado = mis_productos.annotate(
            valor_por_producto=F('precio') * F('stock')
        ).aggregate(valor_total=Sum('valor_por_producto'))
        
        valor_total = resultado['valor_total'] or 0

        if moneda == 'USD':
            tasa = CurrencyService.get_euro_to_dollar_rate()
            valor_total = valor_total * tasa

        return {
            'total': total_articulos,
            'valor': round(valor_total, 2),
            'alertas': alertas,
            'recientes': recientes,
            'moneda': moneda
        }


logger = logging.getLogger(__name__)

class ProductoService:
   
    @staticmethod
    def vender_producto(producto_id, cantidad_vendida=1):
        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            logger.error(f"Intento de compra fallido: Producto ID {producto_id} no encontrado.")
            raise ValidationError("El producto no existe.")
        
        # Lógica de negocio: No vendemos si no hay stock
        if producto.stock < cantidad_vendida:
            raise ValidationError(f"No hay suficiente stock para {producto.nombre}")
        
        producto.stock -= cantidad_vendida
        producto.save()

        if producto.stock == 0:
            logger.warning(f"Intento de compra sin stock. Producto: {producto.nombre}")
            avisar_admin_sin_stock.delay(producto.nombre)
        
        logger.info(f"Venta exitosa: {producto.nombre}. Stock restante: {producto.stock}")

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
        

# Configuramos un logger para avisarnos si la API falla
logger = logging.getLogger(__name__)

class CurrencyService:
    # Usaremos una API gratuita (puedes registrarte en ExchangeRate-API o similar)
    API_URL = "https://open.er-api.com/v6/latest/EUR"

    @staticmethod
    def get_euro_to_dollar_rate():
        try:
            # 🚀 El timeout es vital: si la API externa está lenta, 
            # no queremos que nuestra web se quede colgada 20 segundos.
            response = requests.get(CurrencyService.API_URL, timeout=5)
            response.raise_for_status() # Lanza error si el servidor devuelve un 404 o 500
            
            data = response.json()
            return data['rates']['USD']
            
        except (requests.RequestException, KeyError) as e:
            # Si la API falla, registramos el error y damos un valor por defecto
            # para que la app no explote.
            logger.error(f"Error consultando la API de moneda: {e}")
            return 1.08  # Valor de "emergencia" (fallback)

        