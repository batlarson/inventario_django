from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto

class VentaRapidaTests(APITestCase):
    
    # 1. setUp: Aquí preparamos la "base de datos fantasma"
    def setUp(self):
        # Creamos un usuario de prueba
        self.user = User.objects.create_user(username='entrevista_test', password='password_123')
        
        # Creamos un producto de prueba con stock 5
        self.producto = Producto.objects.create(
            nombre='Teclado Mecánico',
            precio=50.0,
            stock=5,
            usuario=self.user
        )
        
        # Le decimos a la prueba que "inicie sesión" con este usuario
        self.client.force_authenticate(user=self.user)

    # 2. El Test "Feliz": Probamos que una venta normal funciona
    def test_venta_rapida_baja_stock(self):
        # Obtenemos la URL exacta usando el "name" que le diste en urls.py
        url = reverse('api_detalle', kwargs={'pk': self.producto.id})
        
        # Simulamos que el JavaScript envía un PATCH con stock 4
        data = {'stock': 4}
        response = self.client.patch(url, data)
        
        # COMPROBACIONES (Asserts)
        # ¿El servidor respondió con un 200 OK?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ¿El stock en la respuesta es realmente 4?
        self.assertEqual(response.data['stock'], 4)

    def test_venta_rapida_sin_stock(self):
        # Primero, ponemos el stock del producto a 0 a la fuerza para la prueba
        self.producto.stock = 0
        self.producto.save()

        url = reverse('api_detalle', kwargs={'pk': self.producto.id})
        
        # Hacemos la petición (da igual lo que enviemos en 'data', el servicio lo ignora)
        response = self.client.patch(url, {})
        
        # COMPROBACIONES
        # ¿El servidor nos paró los pies con un 400 Bad Request?
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

