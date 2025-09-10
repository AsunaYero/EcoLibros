from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction, models
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import json

from .models import Libro, Categoria, Carrito, ItemCarrito, Pedido, ItemPedido
from .forms import PedidoForm


def obtener_o_crear_carrito(request):
    """Obtiene el carrito del usuario o crea uno nuevo"""
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        carrito, created = Carrito.objects.get_or_create(session_key=session_key)
    return carrito


def index(request):
    """Página principal con catálogo de libros"""
    categorias = Categoria.objects.all()
    libros_destacados = Libro.objects.filter(activo=True, stock__gt=0)[:8]
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('busqueda')
    
    libros = Libro.objects.filter(activo=True, stock__gt=0)
    
    if categoria_id:
        libros = libros.filter(categoria_id=categoria_id)
    
    if busqueda:
        libros = libros.filter(
            models.Q(titulo__icontains=busqueda) | 
            models.Q(autor__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(libros, 12)
    page_number = request.GET.get('page')
    libros_paginados = paginator.get_page(page_number)
    
    # Obtener carrito para mostrar cantidad
    carrito = obtener_o_crear_carrito(request)
    
    context = {
        'libros_destacados': libros_destacados,
        'libros': libros_paginados,
        'categorias': categorias,
        'categoria_actual': categoria_id,
        'busqueda_actual': busqueda,
        'cantidad_carrito': carrito.cantidad_total,
    }
    return render(request, 'tienda/index.html', context)


def detalle_libro(request, libro_id):
    """Detalle de un libro específico"""
    libro = get_object_or_404(Libro, id=libro_id, activo=True)
    libros_relacionados = Libro.objects.filter(
        categoria=libro.categoria, 
        activo=True, 
        stock__gt=0
    ).exclude(id=libro_id)[:4]
    
    carrito = obtener_o_crear_carrito(request)
    
    context = {
        'libro': libro,
        'libros_relacionados': libros_relacionados,
        'cantidad_carrito': carrito.cantidad_total,
    }
    return render(request, 'tienda/detalle_libro.html', context)


@require_POST
def agregar_al_carrito(request, libro_id):
    """Agrega un libro al carrito"""
    libro = get_object_or_404(Libro, id=libro_id, activo=True)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad <= 0:
        return JsonResponse({'error': 'La cantidad debe ser mayor a 0'}, status=400)
    
    if cantidad > libro.stock:
        return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
    
    carrito = obtener_o_crear_carrito(request)
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        libro=libro,
        defaults={'cantidad': cantidad}
    )
    
    if not created:
        item.cantidad += cantidad
        if item.cantidad > libro.stock:
            return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
        item.save()
    
    return JsonResponse({
        'success': True,
        'mensaje': f'{libro.titulo} agregado al carrito',
        'cantidad_carrito': carrito.cantidad_total
    })


def ver_carrito(request):
    """Muestra el contenido del carrito"""
    carrito = obtener_o_crear_carrito(request)
    items = carrito.items.all()
    
    context = {
        'carrito': carrito,
        'items': items,
        'cantidad_carrito': carrito.cantidad_total,
    }
    return render(request, 'tienda/carrito.html', context)


@require_POST
def actualizar_carrito(request, item_id):
    """Actualiza la cantidad de un item en el carrito"""
    item = get_object_or_404(ItemCarrito, id=item_id)
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    
    if nueva_cantidad <= 0:
        item.delete()
        return JsonResponse({'success': True, 'mensaje': 'Item eliminado del carrito'})
    
    if nueva_cantidad > item.libro.stock:
        return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
    
    item.cantidad = nueva_cantidad
    item.save()
    
    return JsonResponse({
        'success': True,
        'subtotal': float(item.subtotal),
        'total': float(item.carrito.total)
    })


@require_POST
def eliminar_del_carrito(request, item_id):
    """Elimina un item del carrito"""
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    
    return JsonResponse({
        'success': True,
        'mensaje': 'Item eliminado del carrito',
        'total': float(item.carrito.total)
    })


def checkout(request):
    """Proceso de checkout"""
    carrito = obtener_o_crear_carrito(request)
    items = carrito.items.all()
    
    if not items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('ver_carrito')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Crear el pedido
                pedido = form.save(commit=False)
                if request.user.is_authenticated:
                    pedido.usuario = request.user
                
                # Calcular totales
                subtotal = carrito.total
                impuestos = subtotal * Decimal('0.19')  # 19% IVA
                total = subtotal + impuestos
                
                pedido.subtotal = subtotal
                pedido.impuestos = impuestos
                pedido.total = total
                pedido.save()
                
                # Crear items del pedido y actualizar stock
                for item in items:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        libro=item.libro,
                        cantidad=item.cantidad,
                        precio_unitario=item.libro.precio
                    )
                    
                    # Actualizar stock
                    item.libro.stock -= item.cantidad
                    item.libro.save()
                
                # Limpiar carrito
                items.delete()
                
                messages.success(request, f'Pedido #{pedido.id} creado exitosamente')
                return redirect('confirmacion_pedido', pedido_id=pedido.id)
    else:
        # Pre-llenar formulario si el usuario está autenticado
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
            }
        form = PedidoForm(initial=initial_data)
    
    context = {
        'form': form,
        'carrito': carrito,
        'items': items,
        'cantidad_carrito': carrito.cantidad_total,
    }
    return render(request, 'tienda/checkout.html', context)


def confirmacion_pedido(request, pedido_id):
    """Página de confirmación del pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    context = {
        'pedido': pedido,
        'cantidad_carrito': 0,  # Carrito ya está vacío
    }
    return render(request, 'tienda/confirmacion_pedido.html', context)


@login_required
def mis_pedidos(request):
    """Lista de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context = {
        'pedidos': pedidos,
        'cantidad_carrito': obtener_o_crear_carrito(request).cantidad_total,
    }
    return render(request, 'tienda/mis_pedidos.html', context)


@login_required
def detalle_pedido(request, pedido_id):
    """Detalle de un pedido específico"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    context = {
        'pedido': pedido,
        'cantidad_carrito': obtener_o_crear_carrito(request).cantidad_total,
    }
    return render(request, 'tienda/detalle_pedido.html', context)


# Vistas para el panel de administración (vendedor)
@login_required
def panel_vendedor(request):
    """Panel principal del vendedor"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('index')
    
    # Estadísticas básicas
    total_libros = Libro.objects.count()
    libros_activos = Libro.objects.filter(activo=True).count()
    libros_sin_stock = Libro.objects.filter(stock=0).count()
    
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    pedidos_hoy = Pedido.objects.filter(fecha_creacion__date=timezone.now().date()).count()
    
    # Ventas del mes actual
    from django.db.models import Sum
    ventas_mes = Pedido.objects.filter(
        fecha_creacion__month=timezone.now().month,
        fecha_creacion__year=timezone.now().year,
        estado__in=['procesando', 'enviado', 'entregado']
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Últimos pedidos
    ultimos_pedidos = Pedido.objects.order_by('-fecha_creacion')[:10]
    
    context = {
        'total_libros': total_libros,
        'libros_activos': libros_activos,
        'libros_sin_stock': libros_sin_stock,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_hoy': pedidos_hoy,
        'ventas_mes': ventas_mes,
        'ultimos_pedidos': ultimos_pedidos,
    }
    return render(request, 'tienda/panel_vendedor.html', context)


@login_required
def reportes_ventas(request):
    """Reportes de ventas"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('index')
    
    # Aquí puedes agregar más lógica para reportes avanzados
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Ventas por mes (últimos 12 meses)
    ventas_por_mes = []
    for i in range(12):
        fecha = timezone.now() - timedelta(days=30*i)
        ventas = Pedido.objects.filter(
            fecha_creacion__month=fecha.month,
            fecha_creacion__year=fecha.year,
            estado__in=['procesando', 'enviado', 'entregado']
        ).aggregate(
            total=Sum('total'),
            cantidad=Count('id')
        )
        ventas_por_mes.append({
            'mes': fecha.strftime('%Y-%m'),
            'total': ventas['total'] or 0,
            'cantidad': ventas['cantidad'] or 0
        })
    
    # Libros más vendidos
    libros_vendidos = ItemPedido.objects.values('libro__titulo').annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos=Sum('precio_unitario')
    ).order_by('-cantidad_vendida')[:10]
    
    context = {
        'ventas_por_mes': ventas_por_mes,
        'libros_vendidos': libros_vendidos,
    }
    return render(request, 'tienda/reportes_ventas.html', context)
