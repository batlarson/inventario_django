from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Producto, Historial, User

@receiver(post_save, sender=Producto)
def registrar_creacion_producto(sender, instance, created, **kwargs):
    if created:
        Historial.objects.create(
            accion=f"Se ha creado un nuevo producto: {instance.nombre}"
        )

