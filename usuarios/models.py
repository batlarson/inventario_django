from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

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
