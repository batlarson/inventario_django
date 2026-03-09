from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from .ia_logic import predecir_reabastecimiento

def bienvenida(request):
    return render(request, 'productos/bienvenida.html')

def listado_productos(request):
    todos = Producto.objects.all()
    criticos = Producto.objects.filter(stock__lt=10)
    
    for p in todos:
        p.prediccion = predecir_reabastecimiento(p.stock, p.precio)
    
    contexto = {
        'productos': todos,
        'critico': criticos,
        'cantidad': todos.count()
    }
    return render(request, 'productos/lista.html', contexto)

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear.html', {'form': form})

@login_required
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listado')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/crear.html', {'form': form, 'editando': True})

@login_required
def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'El producto "{producto.nombre}" ha sido eliminado correctamente.')
        return redirect('listado')

    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})