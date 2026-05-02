from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import PerfilSerializer

class PerfilUsuarioAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PerfilSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.perfil