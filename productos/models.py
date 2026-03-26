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

    def __str__(self):
        return self.nombre
    
# 1. Borrar archivo cuando se elimina el objeto Producto
@receiver(post_delete, sender=Producto)
def borrar_imagen_post_delete(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)

# 2. Borrar archivo antiguo cuando se cambia por uno nuevo (Edit)
@receiver(pre_save, sender=Producto)
def borrar_imagen_al_cambiar(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        viejo_producto = Producto.objects.get(pk=instance.pk)
    except Producto.DoesNotExist:
        return False

    nueva_imagen = instance.imagen
    vieja_imagen = viejo_producto.imagen

    if vieja_imagen and vieja_imagen != nueva_imagen:
        if os.path.isfile(vieja_imagen.path):
            os.remove(vieja_imagen.path)
    
class Historial(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='perfiles/', default='perfiles/default.png')
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
@receiver(pre_save, sender=Perfil)
def borrar_avatar_viejo_al_cambiar(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        viejo_perfil = Perfil.objects.get(pk=instance.pk)
    except Perfil.DoesNotExist:
        return False

    if viejo_perfil.avatar and viejo_perfil.avatar != instance.avatar:
        if os.path.isfile(viejo_perfil.avatar.path):
            os.remove(viejo_perfil.avatar.path)

@receiver(post_delete, sender=Perfil)
def borrar_avatar_al_eliminar_perfil(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)