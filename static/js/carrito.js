document.addEventListener('DOMContentLoaded', () => {
    const carrito = JSON.parse(sessionStorage.getItem('carrito')) || []; // Cargar carrito desde sessionStorage
    const tbody = document.querySelector('.cartTable tbody');
    const subtotalElement = document.querySelector('.subtotal');
    const btnAgregar = document.getElementById('btnAgregar'); // Botón para agregar más productos
    const btnComprar = document.getElementById('btnComprar'); // Botón para comprar ahora

    // Métodos de pago
    const creditCardOption = document.getElementById('creditCardOption');
    const giftCardOption = document.getElementById('giftCardOption');
    const bankTransferOption = document.getElementById('bankTransferOption');

    const creditCardForm = document.getElementById('creditCardForm');
    const giftCardForm = document.getElementById('giftCardForm');

    const submitCreditCard = document.getElementById('submitCreditCard');
    const submitGiftCard = document.getElementById('submitGiftCard');

    // Inicializar el carrito
    function actualizarCarrito() {
        tbody.innerHTML = ''; // Vaciar la tabla

        if (carrito.length === 0) {
            const filaVacia = document.createElement('tr');
            filaVacia.innerHTML = `<td colspan="4" style="text-align: center;">El carrito está vacío</td>`;
            tbody.appendChild(filaVacia);
            subtotalElement.textContent = `Subtotal: $0.00`;
            return;
        }

        let subtotal = 0;

        carrito.forEach((producto, index) => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td><img src="${producto.imagen}" alt="${producto.nombre}" class="productImage"> ${producto.nombre}</td>
                <td>$${producto.precio}</td>
                <td>${producto.cantidad}</td>
                <td>
                    <button class="deleteButton" data-index="${index}">Eliminar</button>
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
            const index = parseInt(e.target.getAttribute('data-index'), 10);
            carrito.splice(index, 1); // Eliminar el producto del carrito
            sessionStorage.setItem('carrito', JSON.stringify(carrito)); // Actualizar sessionStorage
            actualizarCarrito(); // Actualizar la tabla
        }
    });

    // Redirigir al catálogo
    btnAgregar.addEventListener('click', () => {
        window.location.href = '/libreria'; // Ajusta la URL según tu configuración
    });

    // Comprar ahora
    btnComprar.addEventListener('click', () => {
        if (carrito.length === 0) {
            alert('No hay productos en el carrito para comprar.');
        } else {
            alert('¡Compra realizada con éxito!');
            sessionStorage.removeItem('carrito'); // Vaciar el carrito
            subtotalElement.textContent = `Subtotal: $0.00`; // Restablecer subtotal
            actualizarCarrito(); // Actualizar la tabla
        }
    });

    // Métodos de pago
    creditCardOption.addEventListener('change', () => {
        creditCardForm.style.display = 'block';
        giftCardForm.style.display = 'none';
    });

    giftCardOption.addEventListener('change', () => {
        giftCardForm.style.display = 'block';
        creditCardForm.style.display = 'none';
    });

    bankTransferOption.addEventListener('change', () => {
        creditCardForm.style.display = 'none';
        giftCardForm.style.display = 'none';
        alert('La transferencia bancaria no requiere registro adicional.');
    });

    // Guardar tarjeta de crédito
    submitCreditCard.addEventListener('click', async () => {
        const numTarjeta = document.getElementById('numTarjeta').value;
        const nombre = document.getElementById('nombreTarjeta').value;
        const fechaVencimiento = document.getElementById('fechaVencimiento').value;
        const cvv = document.getElementById('cvv').value;

        if (!numTarjeta || !nombre || !fechaVencimiento || !cvv) {
            alert('Todos los campos son obligatorios.');
            return;
        }

        try {
            const response = await fetch('/tarjeta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    num_tarjeta: numTarjeta,
                    id_metodopago: 1, // Ajusta el ID según la lógica
                    nombre: nombre,
                    fecha_vencimiento: fechaVencimiento,
                    cvv: cvv
                })
            });

            if (response.ok) {
                alert('Tarjeta de crédito registrada exitosamente.');
                limpiarFormularioTarjeta();
            } else {
                const errorData = await response.json();
                alert(`Error al registrar la tarjeta: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al registrar la tarjeta.');
        }
    });

    // Guardar gift card
    submitGiftCard.addEventListener('click', async () => {
        const idGift = document.getElementById('idGiftCard').value;
        const saldo = document.getElementById('saldoGiftCard').value;
        const fechaEmision = document.getElementById('fechaEmisionGiftCard').value;
        const fechaExpedicion = document.getElementById('fechaExpedicionGiftCard').value;

        if (!idGift || !saldo || !fechaEmision || !fechaExpedicion) {
            alert('Todos los campos son obligatorios.');
            return;
        }

        try {
            const response = await fetch('/gift_card', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id_gift: idGift,
                    id_metodopago: 1, // Ajusta el ID según la lógica
                    saldo: parseFloat(saldo),
                    fecha_emision: fechaEmision,
                    fecha_expedicion: fechaExpedicion
                })
            });

            if (response.ok) {
                alert('Gift card registrada exitosamente.');
                limpiarFormularioGiftCard();
            } else {
                const errorData = await response.json();
                alert(`Error al registrar la gift card: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al registrar la gift card.');
        }
    });

    // Limpiar formulario de tarjeta de crédito
    function limpiarFormularioTarjeta() {
        document.getElementById('numTarjeta').value = '';
        document.getElementById('nombreTarjeta').value = '';
        document.getElementById('fechaVencimiento').value = '';
        document.getElementById('cvv').value = '';
    }

    // Limpiar formulario de gift card
    function limpiarFormularioGiftCard() {
        document.getElementById('idGiftCard').value = '';
        document.getElementById('saldoGiftCard').value = '';
        document.getElementById('fechaEmisionGiftCard').value = '';
        document.getElementById('fechaExpedicionGiftCard').value = '';
    }

    // Cargar el carrito al cargar la página
    actualizarCarrito();
});
