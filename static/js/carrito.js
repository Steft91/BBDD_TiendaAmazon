document.addEventListener('DOMContentLoaded', () => {
    const carrito = JSON.parse(sessionStorage.getItem('carrito')) || []; // Cargar carrito desde sessionStorage
    const tbody = document.querySelector('.cartTable tbody');
    const subtotalElement = document.querySelector('.subtotal');
    const btnAgregar = document.getElementById('btnAgregar'); // Botón de agregar

    // Inicializar la tabla del carrito vacía o con productos desde sessionStorage
    function actualizarCarrito() {
        tbody.innerHTML = ''; // Vaciar la tabla

        if (carrito.length === 0) {
            // Mostrar un mensaje si el carrito está vacío
            const filaVacia = document.createElement('tr');
            filaVacia.innerHTML = `<td colspan="4" style="text-align: center;">El carrito está vacío</td>`;
            tbody.appendChild(filaVacia);
            subtotalElement.textContent = `Subtotal: $0.00`;
            return;
        }

        // Renderizar productos en la tabla
        let subtotal = 0;

        carrito.forEach((producto) => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td><img src="${producto.imagen}" alt="${producto.nombre}" class="productImage"> ${producto.nombre}</td>
                <td>$${producto.precio}</td>
                <td>${producto.cantidad}</td>
                <td>
                    <button class="deleteButton" data-id="${producto.id}">Eliminar</button>
                </td>
            `;
            tbody.appendChild(fila);

            subtotal += producto.precio * producto.cantidad;
        });

        subtotalElement.textContent = `Subtotal: $${subtotal.toFixed(2)}`;
    }

    // Eliminar producto del carrito
    tbody.addEventListener('click', (e) => {
        if (e.target.classList.contains('deleteButton')) {
            const id = e.target.getAttribute('data-id');
            const index = carrito.findIndex((producto) => producto.id === id);
            if (index !== -1) {
                carrito.splice(index, 1); // Eliminar el producto del carrito
                sessionStorage.setItem('carrito', JSON.stringify(carrito)); // Actualizar sessionStorage
                actualizarCarrito(); // Actualizar la tabla
            }
        }
    });

    // Redirigir el botón "Agregar" a la página de la librería
    btnAgregar.addEventListener('click', () => {
        window.location.href = '/libreria'; // Ajustar la URL según tu configuración
    });

    actualizarCarrito(); // Mostrar productos al cargar la página
});
