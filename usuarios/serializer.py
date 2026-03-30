from rest_framework import serializers
from .models import Perfil
from django.contrib.auth.models import User

class PerfilSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    usuario_fecha = serializers.DateTimeField(source='usuario.date_joined', read_only=True)

    class Meta:
        model = Perfil
        fields = ['usuario', 'usuario_nombre', 'usuario_fecha', 'avatar', 'telefono']
        read_only_fields = ['usuario', 'usuario_nombre', 'usuario_fecha']

        def validate_avatar(self, value):
            if value:
                limit_mb = 2
                if value.size > limit_mb * 1024 * 1024:
                    raise serializers.ValidationError(f"La imagen es demasiado grande. Máximo {limit_mb}MB.")
            return value