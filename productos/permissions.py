from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: 
    - Lectura (GET) para cualquier usuario autenticado.
    - Escritura (POST, PUT, DELETE) solo para staff/admin.
    """
    def has_permission(self, request, view):
        # Si la petición es de "lectura" (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para el resto (cambios), solo si es Staff
        return bool(request.user and request.user.is_staff)