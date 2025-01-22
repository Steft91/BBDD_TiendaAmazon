document.addEventListener('DOMContentLoaded', () => {
    fetchClients();    // Cargar clientes al inicio
    fetchProviders();  // Cargar proveedores al inicio
    fetchCategories(); // Cargar categorías al inicio
    fetchProductos(); 
});


// Función para obtener proveedores desde la API
async function fetchProviders() {
    try {
        const response = await fetch('/providers'); // Endpoint para proveedores
        const providers = await response.json();
        console.log('Proveedores:', providers);
    } catch (error) {
        console.error('Error al obtener los proveedores:', error);
    }
}

// Función para obtener categorías desde la API
async function fetchCategories() {
    try {
        const response = await fetch('/categories'); // Endpoint para categorías
        const categories = await response.json();
        console.log('Categorías:', categories);
    } catch (error) {
        console.error('Error al obtener las categorías:', error);
    }
}

// Función para obtener los productos desde la API y generar las cartas
async function fetchProductos() {
    try {
        const response = await fetch('/productos'); // Llamada al backend
        if (!response.ok) {
            throw new Error(`Error al obtener los productos: ${response.statusText}`);
        }

        const productos = await response.json(); // Convertir la respuesta a JSON
        renderProductos(productos); // Generar las cartas de los productos
    } catch (error) {
        console.error('Error al cargar los productos:', error);
    }
}

// Función para generar dinámicamente las cartas de los productos
function renderProductos(productos) {
    const container = document.getElementById('productosContainer'); // Contenedor de las cartas
    container.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevas cartas

    productos.forEach((producto) => {
        // Crear la estructura de la carta
        const card = document.createElement('div');
        card.classList.add('card');
        card.id = producto.NOMBRE; // Usar el nombre como ID (siempre único)

        // Estructura del header de la carta
        const cardHeader = document.createElement('div');
        cardHeader.classList.add('cardHeader');

        const img = document.createElement('img');
        img.src = producto.IMAGEN; // Usar el atributo IMAGEN de la base de datos
        img.alt = producto.NOMBRE;
        img.classList.add('cardImagen');
        cardHeader.appendChild(img);

        const fondoBoton = document.createElement('div');
        fondoBoton.classList.add('fondoBoton');

        const botonDetalles = document.createElement('button');
        botonDetalles.classList.add('botonDetalles');
        const enlaceDetalles = document.createElement('a');
        enlaceDetalles.href = '#'; // Puedes cambiar esto a un enlace dinámico
        enlaceDetalles.textContent = 'View Details';
        botonDetalles.appendChild(enlaceDetalles);
        fondoBoton.appendChild(botonDetalles);
        cardHeader.appendChild(fondoBoton);

        // Estructura del cuerpo de la carta
        const cardBody = document.createElement('div');
        cardBody.classList.add('cardBody');

        const cardContent = document.createElement('div');
        cardContent.classList.add('cardContent');

        const titulo = document.createElement('h3');
        titulo.classList.add('cardTitulo');
        titulo.textContent = producto.NOMBRE; // Usar el atributo NOMBRE de la base de datos
        cardContent.appendChild(titulo);

        const calificacion = document.createElement('div');
        calificacion.classList.add('cardCalificacion');
        calificacion.textContent = '⭐'.repeat(Math.floor(producto.CALIFICACION)) + '☆'; // Calificación con estrellas
        cardContent.appendChild(calificacion);

        const precio = document.createElement('p');
        precio.classList.add('cardPrecio');
        precio.textContent = `US$ ${producto.PRECIO}`; // Usar el atributo PRECIO de la base de datos
        cardContent.appendChild(precio);

        const descuento = document.createElement('p');
        descuento.classList.add('cardDescuento');
        descuento.textContent = `Ahorra ${producto.DESCUENTO}%`; // Usar el atributo DESCUENTO
        cardContent.appendChild(descuento);

        cardBody.appendChild(cardContent);

        // Agregar header y body a la carta
        card.appendChild(cardHeader);
        card.appendChild(cardBody);

        // Agregar la carta al contenedor
        container.appendChild(card);
    });
}