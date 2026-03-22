from django.urls import path
from . import views

urlpatterns = [
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('listado/', views.listado_productos, name='listado'),
    path('nuevo/', views.crear_producto, name='crear'),
    path('editar/<int:id_producto>/', views.editar_producto, name='editar'),
    path('eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar'),
    path('api/listado/', views.producto_api_list, name='api_listado'),
    path('api/producto/<int:pk>/', views.producto_api_detail, name='api_detalle'),
    path('api/categorias/', views.categoria_api_list, name='api_categorias'),
]