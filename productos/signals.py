from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Producto, Historial
from .ia_logic import predecir_reabastecimiento

@receiver(post_save, sender=Producto)
def registrar_creacion_producto(sender, instance, created, **kwargs):
    if created:
        Historial.objects.create(
            accion=f"Se ha creado un nuevo producto: {instance.nombre}"
        )

@receiver(post_save, sender=Producto)
def vigilar_stock_ia(sender, instance, **kwargs):
    # Cada vez que se guarde un producto, la IA lo analiza
    analisis = predecir_reabastecimiento(instance.stock, instance.precio)
    
    # Si la IA detecta algo CRÍTICO, lo anota en el historial automáticamente
    if "CRÍTICO" in analisis:       
        # Si no había alerta o la última es vieja, creamos una nueva
        Historial.objects.create(
            usuario=instance.usuario,
            accion=f"🤖 IA-SYSTEM: Alerta crítica en '{instance.nombre}'. Razón: {analisis}"
        )
        print(f"⚠️ Alerta de IA generada para {instance.nombre}")