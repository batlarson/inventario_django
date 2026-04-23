from django.core.management.base import BaseCommand
from productos.services import ProductoService 

class Command(BaseCommand):
    help = 'Aumenta el precio de todos los productos un 10% por inflación'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando procesamiento masivo...")

        actualizados = ProductoService.aplicar_inflacion_masiva(porcentaje=10)

        self.stdout.write(
            self.style.SUCCESS(f'¡Éxito! Se actualizaron {actualizados} productos.')
        )