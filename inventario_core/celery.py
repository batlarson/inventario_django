import os
from celery import Celery

# 1. Indicamos dónde están los ajustes de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_backend.settings')

# 2. Creamos la instancia de la aplicación Celery
# Sustituye 'tienda_backend' por el nombre de tu carpeta de proyecto
app = Celery('tienda_backend')

# 3. Le decimos que use la configuración de Django (prefijo CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. ¡SÚPER IMPORTANTE! 
# Esto le dice a Celery que busque automáticamente archivos 'tasks.py' 
# en todas tus apps (como la de productos)
app.autodiscover_tasks()