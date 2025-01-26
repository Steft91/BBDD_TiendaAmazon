document.addEventListener('DOMContentLoaded', async () => {
    const categoriasEndpoint = '/categorias'; // Endpoint de categorías en el backend
    const productosEndpoint = '/productos'; // Endpoint de productos en el backend

    try {
      // Obtener categorías y productos desde el backend
      const [categoriasResponse, productosResponse] = await Promise.all([
        fetch(categoriasEndpoint),
        fetch(productosEndpoint)
      ]);

      const categorias = await categoriasResponse.json();
      const productos = await productosResponse.json();

      const container = document.getElementById('productosContainer');
      
      // Generar tarjetas dinámicamente
      categorias.forEach((categoria) => {
        const header = document.createElement('h2');
        header.textContent = categoria.nombre_categoria;
        container.appendChild(header);

        productos
          .filter((producto) => producto.id_categoria === categoria.id_categoria)
          .forEach((producto) => {
            const card = document.createElement('div');
            card.classList.add('card');

            card.innerHTML = `
              <img src="${producto.imagen}" alt="${producto.nombre}">
              <div class="card-body">
                <h3>${producto.nombre}</h3>
                <p>${producto.descripcion}</p>
                <p>Precio: $${producto.precio}</p>
                <p>Descuento: ${producto.descuento}%</p>
                <p>Calificación: ${producto.calificacion}</p>
              </div>
              <div class="card-footer">
                <button>Comprar</button>
              </div>
            `;

            container.appendChild(card);
          });
      });
    } catch (error) {
      console.error('Error al obtener datos del backend:', error);
    }
  });