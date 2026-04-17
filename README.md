# 🚀 Smart Inventory System con IA Predictiva

Sistema de gestión de inventario desarrollado con **Django** que integra un motor de análisis heurístico para la predicción de reabastecimiento.

## 🌟 Características Principales
* **🤖 Motor IA Heurístico:** Algoritmo que analiza stock y precio para sugerir acciones de reabastecimiento en tiempo real.
* **📄 Reporting Pro:** Generación de informes PDF dinámicos utilizando **ReportLab** con categorización visual de estados críticos.
* **⚙️ Arquitectura de Eventos:** Uso de **Django Signals** para auditoría de stock y gestión automatizada de archivos multimedia.
* **🔌 API REST:** Backend totalmente desacoplado y documentado con **Swagger/OpenAPI**.
* **🐳 Dockerizado:** Entorno de desarrollo listo para desplegar con contenedores.

## 🛠️ Stack Tecnológico
* **Backend:** Python 3.x, Django 5.x
* **API:** Django REST Framework
* **Base de datos:** SQLite (Desarrollo) / PostgreSQL compatible
* **Documentación:** Drf-spectacular (Swagger UI)
* **Reporting:** ReportLab

## 📸 Demo de Funcionalidades
*(Aquí puedes subir capturas de tu PDF y de la lista con badges de colores)*

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

