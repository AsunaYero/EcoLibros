from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    
    # Carrito de compras
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # Proceso de compra
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    
    # Pedidos del usuario
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    
    # Panel del vendedor
    path('vendedor/', views.panel_vendedor, name='panel_vendedor'),
    path('vendedor/reportes/', views.reportes_ventas, name='reportes_ventas'),
]

