from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Busca el token en la cookie en vez del header
        access_token = request.COOKIES.get('access_token')
        
        if access_token is None:
            return None
        
        # Usa la lógica de simplejwt para validarlo
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token