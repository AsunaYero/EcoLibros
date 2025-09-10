#!/usr/bin/env python
"""
Script para cargar datos de ejemplo en la librería online
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VentaLibros.settings')
django.setup()

from tienda.models import Categoria, Libro
from django.core.files import File
from decimal import Decimal

def crear_categorias():
    """Crear categorías de ejemplo"""
    categorias_data = [
        {'nombre': 'Ficción', 'descripcion': 'Novelas de ficción, ciencia ficción y fantasía'},
        {'nombre': 'No Ficción', 'descripcion': 'Biografías, historia, ensayos y libros informativos'},
        {'nombre': 'Tecnología', 'descripcion': 'Libros sobre programación, desarrollo web y tecnología'},
        {'nombre': 'Negocios', 'descripcion': 'Libros sobre emprendimiento, marketing y finanzas'},
        {'nombre': 'Autoayuda', 'descripcion': 'Libros de desarrollo personal y motivación'},
        {'nombre': 'Cocina', 'descripcion': 'Recetas, técnicas culinarias y gastronomía'},
        {'nombre': 'Arte y Diseño', 'descripcion': 'Libros sobre arte, diseño gráfico y creatividad'},
        {'nombre': 'Salud y Bienestar', 'descripcion': 'Libros sobre salud, fitness y bienestar personal'},
    ]
    
    categorias_creadas = []
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        categorias_creadas.append(categoria)
        if created:
            print(f"✓ Categoría creada: {categoria.nombre}")
        else:
            print(f"- Categoría ya existe: {categoria.nombre}")
    
    return categorias_creadas

def crear_libros():
    """Crear libros de ejemplo"""
    libros_data = [
        {
            'titulo': 'El Quijote de la Mancha',
            'autor': 'Miguel de Cervantes',
            'descripcion': 'La obra cumbre de la literatura española y una de las más importantes de la literatura universal.',
            'precio': Decimal('25000'),
            'categoria': 'Ficción',
            'stock': 15,
            'isbn': '978-84-376-0494-7'
        },
        {
            'titulo': 'Cien Años de Soledad',
            'autor': 'Gabriel García Márquez',
            'descripcion': 'Una obra maestra del realismo mágico que narra la historia de la familia Buendía.',
            'precio': Decimal('35000'),
            'categoria': 'Ficción',
            'stock': 12,
            'isbn': '978-84-376-0494-8'
        },
        {
            'titulo': 'Python para Principiantes',
            'autor': 'John Smith',
            'descripcion': 'Aprende Python desde cero con ejemplos prácticos y ejercicios.',
            'precio': Decimal('45000'),
            'categoria': 'Tecnología',
            'stock': 20,
            'isbn': '978-84-376-0494-9'
        },
        {
            'titulo': 'Django Web Development',
            'autor': 'Jane Doe',
            'descripcion': 'Desarrollo web profesional con Django. Desde conceptos básicos hasta aplicaciones avanzadas.',
            'precio': Decimal('55000'),
            'categoria': 'Tecnología',
            'stock': 8,
            'isbn': '978-84-376-0495-0'
        },
        {
            'titulo': 'El Arte de la Guerra',
            'autor': 'Sun Tzu',
            'descripcion': 'Tratado militar chino que se ha convertido en una guía para la estrategia empresarial.',
            'precio': Decimal('20000'),
            'categoria': 'Negocios',
            'stock': 25,
            'isbn': '978-84-376-0495-1'
        },
        {
            'titulo': 'Padre Rico, Padre Pobre',
            'autor': 'Robert Kiyosaki',
            'descripcion': 'Una guía para la libertad financiera y el éxito en los negocios.',
            'precio': Decimal('40000'),
            'categoria': 'Negocios',
            'stock': 18,
            'isbn': '978-84-376-0495-2'
        },
        {
            'titulo': 'Los 7 Hábitos de la Gente Altamente Efectiva',
            'autor': 'Stephen Covey',
            'descripcion': 'Principios fundamentales para el desarrollo personal y profesional.',
            'precio': Decimal('38000'),
            'categoria': 'Autoayuda',
            'stock': 22,
            'isbn': '978-84-376-0495-3'
        },
        {
            'titulo': 'El Poder del Ahora',
            'autor': 'Eckhart Tolle',
            'descripcion': 'Una guía espiritual para la transformación de la conciencia.',
            'precio': Decimal('32000'),
            'categoria': 'Autoayuda',
            'stock': 14,
            'isbn': '978-84-376-0495-4'
        },
        {
            'titulo': 'JavaScript: The Good Parts',
            'autor': 'Douglas Crockford',
            'descripcion': 'Una guía para los aspectos más útiles y elegantes del lenguaje JavaScript.',
            'precio': Decimal('48000'),
            'categoria': 'Tecnología',
            'stock': 16,
            'isbn': '978-84-376-0495-5'
        },
        {
            'titulo': 'Clean Code',
            'autor': 'Robert C. Martin',
            'descripcion': 'Un manual para escribir código limpio, legible y mantenible.',
            'precio': Decimal('52000'),
            'categoria': 'Tecnología',
            'stock': 10,
            'isbn': '978-84-376-0495-6'
        },
        {
            'titulo': 'Sapiens: De Animales a Dioses',
            'autor': 'Yuval Noah Harari',
            'descripcion': 'Una exploración fascinante de la historia de la humanidad.',
            'precio': Decimal('42000'),
            'categoria': 'No Ficción',
            'stock': 19,
            'isbn': '978-84-376-0495-7'
        },
        {
            'titulo': 'El Arte de Cocinar',
            'autor': 'Julia Child',
            'descripcion': 'Técnicas clásicas de cocina francesa explicadas paso a paso.',
            'precio': Decimal('60000'),
            'categoria': 'Cocina',
            'stock': 7,
            'isbn': '978-84-376-0495-8'
        },
        {
            'titulo': 'Diseño Gráfico: Principios y Práctica',
            'autor': 'Robin Williams',
            'descripcion': 'Fundamentos del diseño gráfico con ejemplos prácticos.',
            'precio': Decimal('47000'),
            'categoria': 'Arte y Diseño',
            'stock': 13,
            'isbn': '978-84-376-0495-9'
        },
        {
            'titulo': 'Yoga para Principiantes',
            'autor': 'Sarah Johnson',
            'descripcion': 'Una introducción completa al yoga con posturas y técnicas de respiración.',
            'precio': Decimal('28000'),
            'categoria': 'Salud y Bienestar',
            'stock': 21,
            'isbn': '978-84-376-0496-0'
        },
        {
            'titulo': 'Atomic Habits',
            'autor': 'James Clear',
            'descripcion': 'Cómo construir buenos hábitos y romper los malos.',
            'precio': Decimal('36000'),
            'categoria': 'Autoayuda',
            'stock': 17,
            'isbn': '978-84-376-0496-1'
        }
    ]
    
    libros_creados = []
    for libro_data in libros_data:
        try:
            categoria = Categoria.objects.get(nombre=libro_data['categoria'])
            libro, created = Libro.objects.get_or_create(
                titulo=libro_data['titulo'],
                autor=libro_data['autor'],
                defaults={
                    'descripcion': libro_data['descripcion'],
                    'precio': libro_data['precio'],
                    'categoria': categoria,
                    'stock': libro_data['stock'],
                    'isbn': libro_data['isbn'],
                    'activo': True
                }
            )
            libros_creados.append(libro)
            if created:
                print(f"✓ Libro creado: {libro.titulo} - {libro.autor}")
            else:
                print(f"- Libro ya existe: {libro.titulo} - {libro.autor}")
        except Categoria.DoesNotExist:
            print(f"✗ Error: Categoría '{libro_data['categoria']}' no encontrada para {libro_data['titulo']}")
    
    return libros_creados

def main():
    """Función principal"""
    print("🚀 Iniciando carga de datos de ejemplo...")
    print("=" * 50)
    
    # Crear categorías
    print("\n📚 Creando categorías...")
    categorias = crear_categorias()
    
    # Crear libros
    print("\n📖 Creando libros...")
    libros = crear_libros()
    
    print("\n" + "=" * 50)
    print("✅ Carga de datos completada!")
    print(f"📊 Resumen:")
    print(f"   - Categorías: {len(categorias)}")
    print(f"   - Libros: {len(libros)}")
    print("\n🌐 Puedes acceder a la aplicación en: http://127.0.0.1:8000/")
    print("🔧 Panel de administración: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    main()

