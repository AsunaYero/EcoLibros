// JavaScript principal para la librería online

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initCarrito();
    initBusqueda();
    initFiltros();
    initFormularios();
    initNotificaciones();
});

// Funcionalidad del carrito
function initCarrito() {
    // Actualizar badge del carrito
    updateCarritoBadge();
    
    // Agregar al carrito
    document.querySelectorAll('.agregar-carrito').forEach(button => {
        button.addEventListener('click', function() {
            const libroId = this.dataset.libroId;
            const cantidad = this.dataset.cantidad || 1;
            agregarAlCarrito(libroId, cantidad);
        });
    });
}

function agregarAlCarrito(libroId, cantidad = 1) {
    const button = document.querySelector(`[data-libro-id="${libroId}"]`);
    const originalText = button.innerHTML;
    
    // Mostrar loading
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Agregando...';
    button.disabled = true;
    
    fetch(`/agregar-carrito/${libroId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `cantidad=${cantidad}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar badge del carrito
            updateCarritoBadge(data.cantidad_carrito);
            
            // Mostrar mensaje de éxito
            mostrarNotificacion('success', data.mensaje);
            
            // Efecto visual en el botón
            button.innerHTML = '<i class="fas fa-check me-1"></i>Agregado';
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-primary');
                button.disabled = false;
            }, 2000);
        } else {
            mostrarNotificacion('error', data.error);
            button.innerHTML = originalText;
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('error', 'Error al agregar el libro al carrito');
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function updateCarritoBadge(cantidad = null) {
    const badge = document.getElementById('carrito-badge');
    if (badge) {
        if (cantidad !== null) {
            badge.textContent = cantidad;
        } else {
            // Obtener cantidad actual del carrito
            fetch('/carrito/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const cantidadElement = doc.querySelector('#carrito-badge');
                if (cantidadElement) {
                    badge.textContent = cantidadElement.textContent;
                }
            })
            .catch(error => console.error('Error al actualizar badge:', error));
        }
        
        // Efecto de animación
        if (parseInt(badge.textContent) > 0) {
            badge.style.animation = 'pulse 0.5s ease-in-out';
            setTimeout(() => {
                badge.style.animation = '';
            }, 500);
        }
    }
}

// Funcionalidad de búsqueda
function initBusqueda() {
    const searchInput = document.querySelector('input[name="busqueda"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    // Auto-búsqueda después de 3 caracteres
                    // this.form.submit();
                }
            }, 500);
        });
        
        // Buscar al presionar Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
        });
    }
}

// Funcionalidad de filtros
function initFiltros() {
    // Filtros de categoría
    document.querySelectorAll('.filter-buttons .btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remover clase active de todos los botones
            document.querySelectorAll('.filter-buttons .btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Agregar clase active al botón clickeado
            this.classList.add('active');
        });
    });
}

// Funcionalidad de formularios
function initFormularios() {
    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Formateo de campos
    formatInputFields();
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'Este campo es obligatorio');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validación de email
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Ingresa un email válido');
            isValid = false;
        }
    });
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function formatInputFields() {
    // Formateo de teléfono
    const phoneFields = document.querySelectorAll('input[type="tel"], input[name="telefono"]');
    phoneFields.forEach(field => {
        field.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value.length <= 3) {
                    value = value;
                } else if (value.length <= 6) {
                    value = value.slice(0, 3) + ' ' + value.slice(3);
                } else {
                    value = value.slice(0, 3) + ' ' + value.slice(3, 6) + ' ' + value.slice(6, 10);
                }
            }
            this.value = value;
        });
    });
    
    // Formateo de número de tarjeta
    const cardFields = document.querySelectorAll('input[placeholder*="1234"]');
    cardFields.forEach(field => {
        field.addEventListener('input', function() {
            let value = this.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            this.value = formattedValue;
        });
    });
}

// Sistema de notificaciones
function initNotificaciones() {
    // Crear contenedor de notificaciones si no existe
    if (!document.getElementById('notifications-container')) {
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
}

function mostrarNotificacion(tipo, mensaje, duracion = 5000) {
    const container = document.getElementById('notifications-container');
    const notification = document.createElement('div');
    
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[tipo] || 'alert-info';
    
    const iconClass = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    }[tipo] || 'fas fa-info-circle';
    
    notification.className = `alert ${alertClass} alert-dismissible fade show notification`;
    notification.innerHTML = `
        <i class="${iconClass} me-2"></i>
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // Auto-remover después del tiempo especificado
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duracion);
}

// Utilidades
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Funciones para el carrito
function actualizarCantidadCarrito(itemId, nuevaCantidad) {
    if (nuevaCantidad < 1) {
        eliminarItemCarrito(itemId);
        return;
    }
    
    fetch(`/actualizar-carrito/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `cantidad=${nuevaCantidad}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar subtotal del item
            const subtotalElement = document.querySelector(`[data-item-id="${itemId}"]`);
            if (subtotalElement) {
                subtotalElement.textContent = formatCurrency(data.subtotal);
            }
            
            // Actualizar totales
            actualizarTotalesCarrito();
            
            // Actualizar badge del carrito
            updateCarritoBadge(data.cantidad_carrito);
        } else {
            mostrarNotificacion('error', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('error', 'Error al actualizar el carrito');
    });
}

function eliminarItemCarrito(itemId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este libro del carrito?')) {
        return;
    }
    
    fetch(`/eliminar-carrito/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remover fila de la tabla
            const itemRow = document.getElementById(`item-${itemId}`);
            if (itemRow) {
                itemRow.remove();
            }
            
            // Actualizar totales
            actualizarTotalesCarrito();
            
            // Actualizar badge del carrito
            updateCarritoBadge(data.cantidad_carrito);
            
            // Verificar si el carrito está vacío
            const tbody = document.querySelector('tbody');
            if (tbody && tbody.children.length === 0) {
                location.reload();
            }
        } else {
            mostrarNotificacion('error', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('error', 'Error al eliminar el libro del carrito');
    });
}

function actualizarTotalesCarrito() {
    // Recalcular totales basado en los subtotales actuales
    let subtotal = 0;
    document.querySelectorAll('.subtotal').forEach(element => {
        const valor = parseFloat(element.textContent.replace(/[$,]/g, ''));
        subtotal += valor;
    });
    
    const iva = subtotal * 0.19;
    const total = subtotal + iva;
    
    const subtotalElement = document.getElementById('subtotal');
    const ivaElement = document.getElementById('iva');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) subtotalElement.textContent = formatCurrency(subtotal);
    if (ivaElement) ivaElement.textContent = formatCurrency(iva);
    if (totalElement) totalElement.textContent = formatCurrency(total);
}

// Funciones para el proceso de pago
function mostrarInfoPago(metodo) {
    const infoPago = document.getElementById('info-pago');
    const pagoTarjeta = document.getElementById('pago-tarjeta');
    const pagoPse = document.getElementById('pago-pse');
    const pagoEfectivo = document.getElementById('pago-efectivo');
    
    if (metodo) {
        infoPago.style.display = 'block';
        
        // Ocultar todos los métodos
        [pagoTarjeta, pagoPse, pagoEfectivo].forEach(element => {
            if (element) element.style.display = 'none';
        });
        
        // Mostrar el método seleccionado
        if (metodo === 'tarjeta' && pagoTarjeta) {
            pagoTarjeta.style.display = 'block';
        } else if (metodo === 'pse' && pagoPse) {
            pagoPse.style.display = 'block';
        } else if (metodo === 'efectivo' && pagoEfectivo) {
            pagoEfectivo.style.display = 'block';
        }
    } else {
        if (infoPago) infoPago.style.display = 'none';
    }
}

// Animaciones CSS
function addAnimation(element, animationClass) {
    element.classList.add(animationClass);
    setTimeout(() => {
        element.classList.remove(animationClass);
    }, 1000);
}

// Lazy loading para imágenes
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Inicializar lazy loading si está disponible
if ('IntersectionObserver' in window) {
    initLazyLoading();
}

// Exportar funciones para uso global
window.agregarAlCarrito = agregarAlCarrito;
window.actualizarCantidadCarrito = actualizarCantidadCarrito;
window.eliminarItemCarrito = eliminarItemCarrito;
window.mostrarNotificacion = mostrarNotificacion;
window.mostrarInfoPago = mostrarInfoPago;
