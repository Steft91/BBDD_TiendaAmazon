document.addEventListener('DOMContentLoaded', async () => {
    const categoriasEndpoint = '/categorias'; // Endpoint para obtener las categorías
    const productosEndpoint = '/productos'; // Endpoint para obtener los productos
    const addModal = document.getElementById('addModal');
    const addButton = document.getElementById('addButton');
    const closeModalAdd = document.getElementById('closeModalAdd');
    const cancelAdd = document.getElementById('cancelAdd');
    const saveAdd = document.getElementById('saveAdd');
    const addForm = document.getElementById('addForm');
    try {
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
                <button 
                  class="viewButton" 
                  data-id="${producto.id_producto}" 
                  data-nombre="${producto.nombre}" 
                  data-descripcion="${producto.descripcion}" 
                  data-precio="${producto.precio}" 
                  data-stock="${producto.stock}"
                  data-proveedor="${producto.id_proveedor}"
                  data-descuento="${producto.descuento}"
                  data-imagen="${producto.imagen}">
                  
                  View Detalles
                </button>
              </div>
              <div class="card-footer">
                <button 
                  class="buyButton" 
                  data-id="${producto.id_producto}" 
                  data-nombre="${producto.nombre}" 
                  data-precio="${producto.precio}" 
                  data-imagen="${producto.imagen}">
                  Comprar
                </button>
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
  
      // Escuchar clics en los botones "view detalles"
      container.addEventListener('click', (e) => {
        if (e.target.classList.contains('viewButton')) {
          const id = e.target.getAttribute('data-id');
          const nombre = e.target.getAttribute('data-nombre');
          const descripcion = e.target.getAttribute('data-descripcion');
          const precio = e.target.getAttribute('data-precio');
          const imagen = e.target.getAttribute('data-imagen');  
          const stock = e.target.getAttribute('data-stock');
          const proveedor = e.target.getAttribute('data-proveedor');
          const descuento = e.target.getAttribute('data-descuento');
          redirigirADetallesProducto({ id, nombre, descripcion, precio, imagen, stock,proveedor, descuento });
        }
      });
    } catch (error) {
      console.error('Error al obtener datos del backend:', error);
    }
  
    // Agregar un producto al carrito y redirigir a la página del carrito
    function agregarProductoAlCarrito(producto) {
      const carrito = JSON.parse(sessionStorage.getItem('carrito')) || []; // Cargar carrito actual
  
      // Agregar el producto como nuevo elemento en el carrito
      carrito.push({ ...producto, cantidad: 1 });
  
      sessionStorage.setItem('carrito', JSON.stringify(carrito)); // Guardar el carrito actualizado en sessionStorage
      window.location.href = '/carrito'; // Redirigir a la página del carrito
    }
  
    // Redirigir a la página de detalles y pasar los datos del producto
    function redirigirADetallesProducto(producto) {
      sessionStorage.setItem('productoSeleccionado', JSON.stringify(producto)); // Guardar el producto en sessionStorage
      window.location.href = '/libros'; // Redirigir al endpoint correspondiente en Flask
    }

      // Abrir modal para añadir producto
    addButton.addEventListener('click', () => {
      addModal.classList.add('show');
  });

  // Cerrar modal al presionar cancelar o cerrar
  closeModalAdd.addEventListener('click', () => {
      addModal.classList.remove('show');
  });

  cancelAdd.addEventListener('click', () => {
      addModal.classList.remove('show');
  });

  // Guardar nuevo producto
  saveAdd.addEventListener('click', async () => {
      const newProduct = {
          nombre: document.getElementById('addName').value,
          descripcion: document.getElementById('addDescription').value,
          precio: parseFloat(document.getElementById('addPrice').value),
          stock: parseInt(document.getElementById('addStock').value),
          descuento: parseInt(document.getElementById('addDiscount').value),
          id_proveedor: parseInt(document.getElementById('addProvider').value),
          calificacion: 0.0, // Calificación inicial
          id_categoria: 1, // Puedes ajustar este valor según las categorías disponibles
          imagen: "https://via.placeholder.com/150" // Imagen de ejemplo, puedes reemplazarla por un input en el formulario
      };

      // Validar los campos
      if (!newProduct.nombre || !newProduct.descripcion || isNaN(newProduct.precio) || isNaN(newProduct.stock) || isNaN(newProduct.descuento) || isNaN(newProduct.id_proveedor)) {
          alert('Por favor, completa todos los campos correctamente.');
          return;
      }

      try {
          const response = await fetch('/productos', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(newProduct)
          });

          if (response.ok) {
              alert('Producto añadido exitosamente');
              addModal.classList.remove('show');
              addForm.reset(); // Limpiar el formulario
          } else {
              const error = await response.json();
              console.error('Error del servidor:', error);
              alert('Error al añadir el producto: ' + error.message || 'Error desconocido');
          }
      } catch (error) {
          console.error('Error al guardar el producto:', error);
          alert('Error al guardar el producto');
      }
  });
});
  