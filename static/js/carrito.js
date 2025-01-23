const API_URL = "http://localhost:5000/carrito";

// Obtener todos los productos del carrito
async function obtenerCarrito() {
    try {
        const response = await fetch(API_URL);
        const carrito = await response.json();
        renderCarrito(carrito);
    } catch (error) {
        console.error("Error al obtener el carrito:", error);
    }
}

// Renderizar el carrito en la tabla
function renderCarrito(carrito) {
    const tbody = document.querySelector(".cartTable tbody");
    tbody.innerHTML = ""; // Limpiar contenido
    carrito.forEach(item => {
        const row = `
            <tr data-id="${item.id_producto}">
                <td><img src="${item.imagen}" alt="${item.nombre}" class="productImage"> ${item.nombre}</td>
                <td>$${item.precio.toFixed(2)}</td>
                <td>
                    <input type="number" value="${item.cantidad}" min="1" class="quantityInput" data-id="${item.id_producto}">
                </td>
                <td>
                    <button class="btnEliminar" data-id="${item.id_producto}">Eliminar</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    agregarListeners();
}

// Agregar eventos a inputs y botones
function agregarListeners() {
    document.querySelectorAll(".quantityInput").forEach(input => {
        input.addEventListener("change", actualizarCantidad);
    });
    document.querySelectorAll(".btnEliminar").forEach(button => {
        button.addEventListener("click", eliminarProducto);
    });
}

// Actualizar la cantidad de un producto
async function actualizarCantidad(e) {
    const id = e.target.dataset.id;
    const cantidad = e.target.value;
    try {
        await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cantidad: parseInt(cantidad) })
        });
        obtenerCarrito();
    } catch (error) {
        console.error("Error al actualizar la cantidad:", error);
    }
}

// Eliminar un producto del carrito
async function eliminarProducto(e) {
    const id = e.target.dataset.id;
    try {
        await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        obtenerCarrito();
    } catch (error) {
        console.error("Error al eliminar el producto:", error);
    }
}

// Agregar un nuevo producto al carrito
async function agregarProducto(producto) {
    try {
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(producto)
        });
        obtenerCarrito();
    } catch (error) {
        console.error("Error al agregar el producto:", error);
    }
}

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
    obtenerCarrito();
});
