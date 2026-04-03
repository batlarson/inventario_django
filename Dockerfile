# 1. La base: Una imagen de Python oficial y ligera
FROM python:3.12-slim

# 2. Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias (las piezas del mueble)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código del inventario
COPY . /app/

# 6. El comando para arrancar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]