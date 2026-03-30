from django.urls import path
from . import views
from .api_views import PerfilUsuarioAPIView


urlpatterns = [
    path('perfil/', views.editar_perfil, name='perfil'),
    path('api/perfil/', PerfilUsuarioAPIView.as_view(), name='api-perfil'),
]