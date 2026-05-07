from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerfilForm
from django.conf import settings


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,      # JavaScript no puede leerla
                secure=not settings.DEBUG,        # Solo HTTPS
                samesite='Lax',     # Protección CSRF
            )
        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Lee el refresh token de la cookie y lo mete en el request
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=400)
        request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            response.set_cookie(
                key='access_token',
                value=response.data['access'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
            )
        return response

@api_view(['POST'])
def logout_view(request):
    response = Response({'message': 'Logout exitoso'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})
