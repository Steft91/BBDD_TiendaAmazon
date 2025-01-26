// Cargar productos en la tabla al cargar la página
    async function cargarProductos() {
        try {
            const response = await fetch('/productos', { method: 'GET' });
            const productos = await response.json();
            const tbody = document.querySelector('.cartTable tbody');
            tbody.innerHTML = '';

            productos.forEach(producto => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td><img src="${producto.imagen}" alt="${producto.nombre}" class="productImage"> ${producto.nombre}</td>
                    <td>${producto.precio}</td>
                    <td>
                        <input type="number" value="${producto.cantidad}" min="1" class="quantityInput" onchange="editarProducto(${producto.id}, this.value)">
                    </td>
                    <td>
                        <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(fila);
            });
        } catch (error) {
            console.error('Error al cargar productos:', error);
        }
    }

    // Agregar un nuevo producto
    async function agregarProducto() {
        const nombre = prompt('Ingrese el nombre del producto:');
        const precio = parseFloat(prompt('Ingrese el precio del producto:'));
        const cantidad = parseInt(prompt('Ingrese la cantidad del producto:'));

        if (nombre && !isNaN(precio) && !isNaN(cantidad)) {
            try {
                const response = await fetch('/productos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre, precio, cantidad })
                });
                if (response.ok) {
                    alert('Producto agregado exitosamente');
                    cargarProductos();
                } else {
                    alert('Error al agregar producto');
                }
            } catch (error) {
                console.error('Error al agregar producto:', error);
            }
        } else {
            alert('Datos inválidos');
        }
    }

    // Editar un producto existente
    async function editarProducto(id, nuevaCantidad) {
        try {
            const response = await fetch(`/productos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cantidad: nuevaCantidad })
            });
            if (response.ok) {
                alert('Producto actualizado exitosamente');
                cargarProductos();
            } else {
                alert('Error al actualizar producto');
            }
        } catch (error) {
            console.error('Error al actualizar producto:', error);
        }
    }

    // Eliminar un producto
    async function eliminarProducto(id) {
        if (confirm('¿Está seguro de que desea eliminar este producto?')) {
            try {
                const response = await fetch(`/productos/${id}`, { method: 'DELETE' });
                if (response.ok) {
                    alert('Producto eliminado exitosamente');
                    cargarProductos();
                } else {
                    alert('Error al eliminar producto');
                }
            } catch (error) {
                console.error('Error al eliminar producto:', error);
            }
        }
    }

    // Buscar un producto por nombre
    async function buscarProducto() {
        const nombre = prompt('Ingrese el nombre del producto a buscar:');
        if (nombre) {
            try {
                const response = await fetch(`/productos/buscar?nombre=${encodeURIComponent(nombre)}`, { method: 'GET' });
                const productos = await response.json();
                if (productos.length > 0) {
                    const tbody = document.querySelector('.cartTable tbody');
                    tbody.innerHTML = '';
                    productos.forEach(producto => {
                        const fila = document.createElement('tr');
                        fila.innerHTML = `
                            <td><img src="${producto.imagen}" alt="${producto.nombre}" class="productImage"> ${producto.nombre}</td>
                            <td>${producto.precio}</td>
                            <td>${producto.cantidad}</td>
                        `;
                        tbody.appendChild(fila);
                    });
                } else {
                    alert('Producto no encontrado');
                }
            } catch (error) {
                console.error('Error al buscar producto:', error);
            }
        }
    }

    // Asociar botones con las funciones
    document.addEventListener('DOMContentLoaded', () => {
        cargarProductos();
        document.getElementById('btnAgregar').addEventListener('click', agregarProducto);
        document.getElementById('btnBuscar').addEventListener('click', buscarProducto);
    });
