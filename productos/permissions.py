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
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.usuario == request.user