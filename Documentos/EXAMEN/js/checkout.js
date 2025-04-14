// js/checkout.js

// Define la tasa de IVA (ej. 21% para España)
const IVA_RATE = 0.21;

// Elementos donde mostraremos los datos
const checkoutItemsContainer = document.getElementById('checkout-cart-items');
const checkoutSubtotalElement = document.getElementById('checkout-subtotal');
const checkoutIvaElement = document.getElementById('checkout-iva');
const checkoutTotalElement = document.getElementById('checkout-total');

// Función para cargar y mostrar el resumen del carrito
function displayCheckoutCart() {
    // Obtener carrito de localStorage (similar a cart.js, podrías compartir código si estructuras mejor)
    const storedCart = localStorage.getItem('shoppingCart');
    const cart = storedCart ? JSON.parse(storedCart) : [];

    if (!checkoutItemsContainer || !checkoutSubtotalElement || !checkoutIvaElement || !checkoutTotalElement) {
        console.error("Error: Faltan elementos HTML para mostrar el checkout.");
        return;
    }

    checkoutItemsContainer.innerHTML = ''; // Limpiar contenedor
    let subtotal = 0;

    if (cart.length === 0) {
        checkoutItemsContainer.innerHTML = '<p>No hay artículos en tu carrito para procesar.</p>';
        checkoutSubtotalElement.textContent = '0.00';
        checkoutIvaElement.textContent = '0.00';
        checkoutTotalElement.textContent = '0.00';
        return; // Salir si no hay items
    }

    // Crear HTML para cada item y calcular subtotal
    cart.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('checkout-cart-item');
        const itemTotalPrice = (item.price || 0) * (item.quantity || 0);
        subtotal += itemTotalPrice;

        itemElement.innerHTML = `
            <img src="${item.image || 'https://via.placeholder.com/50'}" alt="${item.name || ''}">
            <div class="checkout-cart-item-details">
                <strong>${item.name || 'Producto'}</strong>
                <p>Cantidad: ${item.quantity || 0}</p>
            </div>
            <div class="checkout-cart-item-price">
                €${itemTotalPrice.toFixed(2)}
            </div>
        `;
        checkoutItemsContainer.appendChild(itemElement);
    });

    // Calcular IVA y Total
    const ivaAmount = subtotal * IVA_RATE;
    const total = subtotal + ivaAmount;

    // Mostrar los totales formateados
    checkoutSubtotalElement.textContent = subtotal.toFixed(2);
    checkoutIvaElement.textContent = ivaAmount.toFixed(2);
    checkoutTotalElement.textContent = total.toFixed(2);
}

// Podríamos llamar a displayCheckoutCart directamente al cargar el script,
// pero es mejor hacerlo desde main.js dentro de DOMContentLoaded
// para asegurar que el DOM está listo.
// displayCheckoutCart();