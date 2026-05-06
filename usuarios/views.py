from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerfilForm


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,      # JavaScript no puede leerla
                secure=True,        # Solo HTTPS
                samesite='Lax',     # Protección CSRF
            )
        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,      # JavaScript no puede leerla
                secure=True,        # Solo HTTPS
                samesite='Lax',     # Protección CSRF
            )
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
