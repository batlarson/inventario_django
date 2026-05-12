# 🚀 Smart Inventory System con IA Predictiva

Sistema de gestión de inventario desarrollado con **Django** que integra un motor de análisis heurístico para la predicción de reabastecimiento. Además incluye múltiples APIs REST, testing, signals y deploy con Docker. Caso de producción mientras el servidor esté en funcionamiento: https://inventariodjango-production.up.railway.app/productos/bienvenida

## 🌟 Características Principales
* **🤖 Motor IA Heurístico:** Algoritmo que analiza stock y precio para sugerir acciones de reabastecimiento en tiempo real.
* **🔐 Proteccion JWT:** httpOnly cookies para proteger en envio de data.
* **📄 Reporting Pro:** Generación de informes PDF dinámicos utilizando **ReportLab** con categorización visual de estados críticos.
* **🧪 Testing:** Creacion con usuarios de prueba para probar la seguridad de datos y protección básica de los productos, además de un mock de nuestra "IA".
* **⚙️ Arquitectura de Eventos:** Uso de **Django Signals** para auditoría de stock y gestión automatizada de archivos multimedia.
* **🔌 API REST:** Backend totalmente desacoplado y documentado con **Swagger/OpenAPI**.
* **🐳 Dockerizado:** Entorno de desarrollo listo para desplegar con contenedores.
* **🚀 Produccion:** Desplegado totalmente en railway

## 🛠️ Stack Tecnológico
* **Backend:** Python 3.x, Django 6.x
* **API:** Django REST Framework
* **Base de datos:** SQLite (Desarrollo) / PostgreSQL (Produccion)
* **Documentación:** Drf-spectacular (Swagger UI)
* **Reporting:** ReportLab

## 🧪 Tests
```bash
pytest
```
Incluye tests de seguridad, casos feliz/error y mocks de la lógica IA.

## ⚙️ Variables de entorno
Crea un archivo `.env` en la raíz con estas variables:
```
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=inventario
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=db
DB_PORT=5432
```

## 🚀 Instalación
1. Clonar el repositorio.
2. Ejecutar `docker-compose up --build`.
3. Acceder a `http://localhost:8000`.

## 📁 Estructura Destacada
* `ia_logic.py`: Motor de decisiones con lógica heurística para el cálculo de criticidad.
* `signals.py`: Automatización de procesos (limpieza de archivos y logs de auditoría).
* `views.py`: Implementación de lógica de negocio y generación de buffers para PDFs.

## 🎓 Conceptos Aplicados
* **DRY (Don't Repeat Yourself):** Centralización de lógica en signals y funciones de ayuda.
* **Separación de Responsabilidades:** Lógica de IA aislada de las vistas de Django.
* **Seguridad:** Aislamiento de datos por usuario mediante filtrado en QuerySets (`request.user`).

