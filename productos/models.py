from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)   
    stock = models.IntegerField()
    precio = models.FloatField()
    perecedero = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    #perfil = models.ForeignKey('usuarios.Perfil', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
# 1. Borrar archivo cuando se elimina el objeto Producto
@receiver(post_delete, sender=Producto)
def borrar_imagen_post_delete(sender, instance, **kwargs):
    if instance.imagen:

        if instance.imagen.storage.exists(instance.imagen.name):
            instance.imagen.storage.delete(instance.imagen.name)

@receiver(pre_save, sender=Producto)
def borrar_imagen_al_cambiar(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        viejo_producto = Producto.objects.get(pk=instance.pk)
    except Producto.DoesNotExist:
        return
    
    if viejo_producto.imagen and viejo_producto.imagen.name != instance.imagen.name:
        if viejo_producto.imagen.storage.exists(viejo_producto.imagen.name):
            viejo_producto.imagen.storage.delete(viejo_producto.imagen.name)
    
class Historial(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

