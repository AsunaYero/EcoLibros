from django.contrib import admin
from .models import Categoria, Libro, Carrito, ItemCarrito, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']
    search_fields = ['nombre']
    list_filter = ['fecha_creacion']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'precio', 'stock', 'categoria', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'autor', 'isbn']
    list_editable = ['precio', 'stock', 'activo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'autor', 'descripcion', 'categoria')
        }),
        ('Precio e Inventario', {
            'fields': ('precio', 'stock', 'activo')
        }),
        ('Detalles Adicionales', {
            'fields': ('imagen', 'fecha_publicacion', 'isbn'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_completo', 'email', 'estado', 'total', 'metodo_pago', 'fecha_creacion']
    list_filter = ['estado', 'metodo_pago', 'fecha_creacion']
    search_fields = ['nombre_completo', 'email', 'telefono']
    list_editable = ['estado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('usuario', 'nombre_completo', 'email', 'telefono')
        }),
        ('Dirección de Envío', {
            'fields': ('direccion', 'ciudad', 'codigo_postal')
        }),
        ('Detalles del Pedido', {
            'fields': ('estado', 'metodo_pago', 'subtotal', 'impuestos', 'total', 'notas')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'session_key', 'cantidad_total', 'total', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['usuario__username', 'session_key']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'carrito', 'libro', 'cantidad', 'subtotal', 'fecha_agregado']
    list_filter = ['fecha_agregado']
    search_fields = ['libro__titulo', 'carrito__usuario__username']
    readonly_fields = ['fecha_agregado']


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'libro', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido__fecha_creacion']
    search_fields = ['libro__titulo', 'pedido__nombre_completo']

