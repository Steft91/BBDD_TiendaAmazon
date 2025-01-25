document.addEventListener('DOMContentLoaded', () => {
    fetchCategories(); // Cargar categorías al inicio
    fetchProductos();  // Cargar productos al inicio
});

// Función para obtener categorías desde la API
async function fetchCategories() {
    try {
        const response = await fetch('/categories'); // Endpoint para categorías
        if (!response.ok) {
            throw new Error(`Error al obtener las categorías: ${response.statusText}`);
        }

        const categories = await response.json();
        renderCategories(categories); // Generar la barra lateral de categorías
    } catch (error) {
        console.error('Error al obtener las categorías:', error);
    }
}

// Función para generar dinámicamente la barra lateral de categorías
function renderCategories(categories) {
    const sidebar = document.querySelector('.sidebar ul');
    sidebar.innerHTML = '<h2>Categorías</h2>'; // Limpiar contenido existente y agregar título

    categories.forEach((categoria) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#categoria-${categoria.ID_CATEGORIA}`;
        link.textContent = categoria.NOMBRE;
        li.appendChild(link);
        sidebar.appendChild(li);
    });
}

// Función para obtener los productos desde la API y generar las cartas
async function fetchProductos() {
    try {
        const response = await fetch('/productos'); // Endpoint para productos
        if (!response.ok) {
            throw new Error(`Error al obtener los productos: ${response.statusText}`);
        }

        const productos = await response.json();
        renderProductos(productos); // Generar las cartas de los productos
    } catch (error) {
        console.error('Error al cargar los productos:', error);
    }
}

// Función para generar dinámicamente las cartas de productos
function renderProductos(productos) {
    const container = document.getElementById('productosContainer'); // Contenedor de las cartas
    container.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevas cartas

    // Agrupar productos por categoría
    const productosPorCategoria = productos.reduce((acc, producto) => {
        const categoriaId = producto.ID_CATEGORIA;
        if (!acc[categoriaId]) {
            acc[categoriaId] = [];
        }
        acc[categoriaId].push(producto);
        return acc;
    }, {});

    // Crear secciones por categoría
    Object.keys(productosPorCategoria).forEach((categoriaId) => {
        const categoriaProductos = productosPorCategoria[categoriaId];
        const categoriaTitulo = categoriaProductos[0]?.NOMBRE_CATEGORIA || `Categoría ${categoriaId}`;

        // Crear encabezado de categoría
        const section = document.createElement('section');
        section.id = `categoria-${categoriaId}`;
        section.classList.add('categoria');
        
        const titulo = document.createElement('h2');
        titulo.textContent = categoriaTitulo;
        section.appendChild(titulo);

        // Crear las cartas de los productos de la categoría
        categoriaProductos.forEach((producto) => {
            const card = document.createElement('div');
            card.classList.add('card');

            const cardHeader = document.createElement('div');
            cardHeader.classList.add('cardHeader');

            const img = document.createElement('img');
            img.src = producto.IMAGEN;
            img.alt = producto.NOMBRE;
            img.classList.add('cardImagen');
            cardHeader.appendChild(img);

            const fondoBoton = document.createElement('div');
            fondoBoton.classList.add('fondoBoton');

            const botonDetalles = document.createElement('button');
            botonDetalles.classList.add('botonDetalles');
            const enlaceDetalles = document.createElement('a');
            enlaceDetalles.href = '#'; // Aquí puedes redirigir a una página de detalles del producto
            enlaceDetalles.textContent = 'View Details';
            botonDetalles.appendChild(enlaceDetalles);
            fondoBoton.appendChild(botonDetalles);
            cardHeader.appendChild(fondoBoton);

            const cardBody = document.createElement('div');
            cardBody.classList.add('cardBody');

            const cardContent = document.createElement('div');
            cardContent.classList.add('cardContent');

            const titulo = document.createElement('h3');
            titulo.classList.add('cardTitulo');
            titulo.textContent = producto.NOMBRE;
            cardContent.appendChild(titulo);

            const calificacion = document.createElement('div');
            calificacion.classList.add('cardCalificacion');
            calificacion.textContent = '⭐'.repeat(Math.floor(producto.CALIFICACION)) + '☆';
            cardContent.appendChild(calificacion);

            const precio = document.createElement('p');
            precio.classList.add('cardPrecio');
            precio.textContent = `US$ ${producto.PRECIO}`;
            cardContent.appendChild(precio);

            const descuento = document.createElement('p');
            descuento.classList.add('cardDescuento');
            descuento.textContent = `Ahorra ${producto.DESCUENTO}%`;
            cardContent.appendChild(descuento);

            cardBody.appendChild(cardContent);
            card.appendChild(cardHeader);
            card.appendChild(cardBody);

            section.appendChild(card);
        });

        container.appendChild(section);
    });
}
