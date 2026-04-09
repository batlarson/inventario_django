from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, Sum, F
from .models import Producto, Categoria, Historial
from .forms import ProductoForm
from .ia_logic import predecir_reabastecimiento
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductoSerializer, CategoriaSerializer
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes



@login_required
def bienvenida(request):
    mis_productos = Producto.objects.filter(usuario=request.user)
    
    total_articulos = mis_productos.count()
    
    resultado = mis_productos.annotate(
        valor_por_producto=F('precio') * F('stock')
    ).aggregate(
        valor_total=Sum('valor_por_producto')
    )
    
    valor_total = resultado['valor_total'] or 0
    
    alertas = mis_productos.filter(stock__lt=10).count()

    recientes = Historial.objects.all().order_by('-fecha')[:5]

    contexto = {
        'total': total_articulos,
        'valor': valor_total,
        'alertas': alertas,
        'recientes': recientes,
    }
    return render(request, 'productos/bienvenida.html', contexto)

@login_required
def listado_productos(request):
    productos = Producto.objects.filter(usuario=request.user).select_related('categoria').all()
    categorias = Categoria.objects.all()

    conteo_categorias = productos.values('categoria__nombre').annotate(total=Count('id'))

    labels = [item['categoria__nombre'] or "Sin Categoría" for item in conteo_categorias]
    data = [item['total'] for item in conteo_categorias]
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    nombre_buscar = request.GET.get('buscar')
    if nombre_buscar:
        productos = productos.filter(nombre__icontains=nombre_buscar)

    criticos = productos.filter(stock__lt=10)
    for p in productos:
        p.prediccion = predecir_reabastecimiento(p.stock, p.precio)
    
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'criticos': criticos,
        'cantidad': productos.count(),
        'labels': labels,
        'data': data,
    }
    return render(request, 'productos/lista.html', contexto)

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()
            return redirect('listado')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear.html', {'form': form})

@login_required
def editar_producto(request, id_producto,):
    producto = get_object_or_404(Producto, id=id_producto, usuario=request.user)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            Historial.objects.create(
                usuario=request.user,
                accion=f"EDITADO: {request.user.username} modificó '{producto.nombre}'"
            )
            return redirect('listado')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/crear.html', {'form': form, 'editando': True})

@login_required
def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto, usuario=request.user)
    
    if request.method == 'POST':
        nombre_eliminado = producto.nombre
        producto.delete()
        Historial.objects.create(
            usuario=request.user,
            accion=f"ELIMINADO: {request.user.username} borró el producto '{nombre_eliminado}'"
        )
        messages.success(request, f'El producto "{nombre_eliminado}" ha sido eliminado correctamente.')
        return redirect('listado')

    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})


@extend_schema(
    methods=['GET'],
    responses=ProductoSerializer,
    parameters=[
        OpenApiParameter(
            name='cat', 
            description='Filtrar productos por el ID de la categoría', 
            required=False, 
            type=OpenApiTypes.INT
        ),
    ]
)
@extend_schema(
    methods=['POST'],
    request=ProductoSerializer,
    responses=ProductoSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def producto_api_list(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(usuario=request.user)

        categoria_id = request.query_params.get('cat')
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)

        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['GET'],
    responses={200: ProductoSerializer}
)
@extend_schema(
    methods=['PUT'],
    request=ProductoSerializer,
    responses={200: ProductoSerializer, 400: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT}
)
@extend_schema(
    methods=['DELETE'],
    responses={204: None, 404: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT}
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def producto_api_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk, usuario=request.user)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    methods=['GET'],
    responses=CategoriaSerializer,
)
@extend_schema(
    methods=['POST'],
    request=CategoriaSerializer,
    responses={
        201: CategoriaSerializer,
        403: OpenApiTypes.OBJECT,
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def categoria_api_list(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Obtener recomendaciones de reabastecimiento",
    description="Devuelve solo los productos que la IA considera en estado CRÍTICO o RECOMENDADO.",
    responses={200: ProductoSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Cualquier usuario logueado puede ver qué falta
def recomendaciones_ia(request):
    # 1. Traemos los productos del usuario
    todos_los_productos = Producto.objects.filter(usuario=request.user)
    
    productos_urgentes = []

    # 2. Pasamos el filtro de la IA
    for p in todos_los_productos:
        # Usamos tu nueva función de ia_logic
        resultado = predecir_reabastecimiento(p.stock, p.precio)
        
        # Si la IA dice que es CRÍTICO o RECOMENDADO (lo sabemos por el texto)
        if "CRÍTICO" in resultado or "RECOMENDADO" in resultado:
            # Añadimos un campo extra al objeto solo para esta respuesta
            p.analisis_ia = resultado 
            productos_urgentes.append(p)

    # 3. Serializamos y enviamos
    serializer = ProductoSerializer(productos_urgentes, many=True)
    return Response(serializer.data)