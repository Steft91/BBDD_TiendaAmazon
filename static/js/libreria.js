document.addEventListener('DOMContentLoaded', async () => {
  const categoriasEndpoint = '/categorias'; // Endpoint para obtener las categorías
  const productosEndpoint = '/productos'; // Endpoint para obtener los productos
  const carrito = JSON.parse(sessionStorage.getItem('carrito')) || []; // Inicializar carrito desde sessionStorage

  try {
      // Obtener categorías y productos del backend
      const [categoriasResponse, productosResponse] = await Promise.all([
          fetch(categoriasEndpoint),
          fetch(productosEndpoint),
      ]);

      const categorias = await categoriasResponse.json();
      const productos = await productosResponse.json();

      const container = document.getElementById('productosContainer');

      // Renderizar productos agrupados por categorías
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
                      </div>
                      <div class="card-footer">
                          <button class="buyButton" data-id="${producto.id}" data-nombre="${producto.nombre}" data-precio="${producto.precio}" data-imagen="${producto.imagen}">Comprar</button>
                      </div>
                  `;

                  container.appendChild(card);
              });
      });

      // Escuchar clics en los botones "Comprar"
      container.addEventListener('click', (e) => {
          if (e.target.classList.contains('buyButton')) {
              const id = e.target.getAttribute('data-id');
              const nombre = e.target.getAttribute('data-nombre');
              const precio = parseFloat(e.target.getAttribute('data-precio'));
              const imagen = e.target.getAttribute('data-imagen');

              agregarProductoAlCarrito({ id, nombre, precio, imagen });
          }
      });
  } catch (error) {
      console.error('Error al obtener datos del backend:', error);
  }

  // Agregar un producto al carrito y redirigir a la página del carrito
  function agregarProductoAlCarrito(producto) {
      const productoExistente = carrito.find((item) => item.id === producto.id);

      if (productoExistente) {
          productoExistente.cantidad += 1; // Incrementar la cantidad si el producto ya existe
      } else {
          carrito.push({ ...producto, cantidad: 1 }); // Agregar un nuevo producto al carrito
      }

      sessionStorage.setItem('carrito', JSON.stringify(carrito)); // Guardar el carrito actualizado en sessionStorage
      window.location.href = '/carrito'; // Redirigir a la página del carrito
  }
});
