from django.urls import path
from . import views

urlpatterns = [
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('listado/', views.listado_productos, name='listado'),
    path('nuevo/', views.crear_producto, name='crear'),
    path('editar/<int:id_producto>/', views.editar_producto, name='editar'),
    path('eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar')
]