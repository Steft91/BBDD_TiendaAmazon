document.addEventListener('DOMContentLoaded', () => {
    fetchClients();    // Cargar clientes al inicio
    fetchProviders();  // Cargar proveedores al inicio
    fetchCategories(); // Cargar categorías al inicio
});

// Función para obtener clientes desde la API
async function fetchClients() {
    try {
        const response = await fetch('/clients'); // Endpoint para clientes
        const clients = await response.json();
        console.log('Clientes:', clients);
    } catch (error) {
        console.error('Error al obtener los clientes:', error);
    }
}

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
