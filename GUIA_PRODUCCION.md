# Guía de Producción - Gestor de Inventario Inteligente
## Fecha: 8 de mayo de 2026

### 🔐 Configuraciones de Seguridad para Producción

#### Variables de Entorno (.env.production)
```bash
# Clave secreta fuerte (generar nueva)
SECRET_KEY=tu-clave-muy-segura-de-50-caracteres-minimo-aqui

# Producción = False para debug
DEBUG=False

# Dominios permitidos (cambiar por tu dominio real)
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,api.tu-dominio.com

# Base de datos PostgreSQL
DB_NAME=inventario_prod
DB_USER=inventario_user
DB_PASSWORD=contraseña_muy_segura_aqui
DB_HOST=localhost
DB_PORT=5432

# Redis para cache y Celery
REDIS_URL=redis://localhost:6379/1

# Email configuración
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=app-password-de-gmail
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com

# Configuración adicional para producción
DJANGO_SETTINGS_MODULE=inventario_core.settings.production
```

#### Cambios en settings.py para producción

**Agregar estas configuraciones de seguridad:**
```python
# Seguridad HTTPS (después de ALLOWED_HOSTS)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies seguras
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Headers de seguridad adicionales
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CORS (si necesitas APIs externas)
INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]
```

**Cambiar base de datos a PostgreSQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

**Configuración de email:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

**Cache con Redis:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }
}
```

### 🚀 Proceso de Deployment

#### Opción 1: VPS/Dedicado (Recomendado)
1. **Servidor**: DigitalOcean, Linode, AWS EC2, etc.
2. **Subir código**: `git clone` o `git push` a repositorio
3. **Configurar servicios**:
   - PostgreSQL
   - Redis
   - Nginx
   - SSL (Let's Encrypt)
4. **Variables de entorno**: Configurar en el servidor
5. **Migrar datos**: `python manage.py migrate`

#### Opción 2: Plataformas PaaS
- **Railway**: Fácil, automático
- **Heroku**: Popular, pero caro
- **Render**: Bueno para Django
- **Fly.io**: Moderno, con Docker

#### Opción 3: Docker (Tu setup actual)
- Configurar variables de entorno en docker-compose.prod.yml
- Usar PostgreSQL y Redis en contenedores
- Configurar Nginx reverse proxy

### 📋 Checklist de Producción

- [ ] Generar nueva SECRET_KEY
- [ ] Configurar dominio en ALLOWED_HOSTS
- [ ] Cambiar DEBUG=False
- [ ] Configurar base de datos PostgreSQL
- [ ] Configurar Redis para cache/Celery
- [ ] Configurar email SMTP
- [ ] Habilitar HTTPS
- [ ] Configurar CORS si es necesario
- [ ] Probar todas las funcionalidades
- [ ] Configurar backups automáticos
- [ ] Configurar monitoreo (Sentry opcional)

### 🔧 Comandos Útiles

```bash
# Generar SECRET_KEY segura
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Probar configuración
python manage.py check --deploy

# Crear superusuario
python manage.py createsuperuser

# Migrar base de datos
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### ⚠️ Notas Importantes

1. **Nunca copies .env de desarrollo a producción**
2. **Usa contraseñas diferentes en cada entorno**
3. **Configura backups regulares de la BD**
4. **Monitorea logs de errores**
5. **Mantén dependencias actualizadas**
6. **Usa HTTPS siempre**

---
*Guardado desde conversación con GitHub Copilot - 8 mayo 2026*</content>
<parameter name="filePath">c:\Users\Ibon Mugica\Desktop\Django\Gestor_de_Inventario_Inteligente\GUIA_PRODUCCION.md