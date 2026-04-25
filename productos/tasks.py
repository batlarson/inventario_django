# productos/tasks.py
from celery import shared_task
import time

@shared_task
def avisar_admin_sin_stock(producto_nombre):
    """
    Esta función la ejecuta el 'Worker' (el empleado de fondo).
    El usuario nunca se entera de que esto está pasando.
    """
    print(f"[CELERY] Preparando email de aviso para el jefe...")
    
    # Simulamos que el servidor de correo es lento
    time.sleep(3) 
    
    # Aquí iría el código real de Django para enviar emails (send_mail)
    print(f"[CELERY] 📩 ¡Aviso enviado! El producto '{producto_nombre}' se ha agotado.")
    
    return True