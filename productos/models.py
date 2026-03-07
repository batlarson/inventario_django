from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)   
    stock = models.IntegerField()
    precio = models.FloatField()
    perecedero = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre