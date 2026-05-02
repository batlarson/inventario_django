from django.urls import path
from . import views
from .api_views import PerfilUsuarioAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('perfil/', views.editar_perfil, name='perfil'),
    path('api/perfil/', PerfilUsuarioAPIView.as_view(), name='api-perfil'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]