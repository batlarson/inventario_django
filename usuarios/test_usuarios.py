import pytest
from django.contrib.auth.models import User
from .models import Perfil

@pytest.mark.django_db # Esto le da permiso al test para usar la base de datos
def test_creacion_perfil_automatico_con_signal():
    # 1. ACCIÓN: Creamos un usuario (esto debería disparar nuestra Signal)
    usuario = User.objects.create_user(username="testuser", password="password123")

    # 2. COMPROBACIÓN (Assertion): ¿Se ha creado el perfil?
    existe_perfil = Perfil.objects.filter(usuario=usuario).exists()
    
    # 3. RESULTADO: Si esto es False, el test fallará
    assert existe_perfil is True
    
    # Extra: Comprobamos que el perfil esté vinculado al usuario correcto
    perfil = Perfil.objects.get(usuario=usuario)
    assert perfil.usuario.username == "testuser"