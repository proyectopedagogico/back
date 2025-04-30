document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM completamente cargado y parseado.");

    // Inicializar funcionalidades COMUNES a todas las páginas
    // Asegúrate que estas funciones existan globalmente o estén importadas
    if (typeof initializeTheme === 'function') initializeTheme(); else console.error("initializeTheme no definida");
    if (typeof loadCart === 'function') loadCart(); else console.error("loadCart no definida");
    if (typeof updateAuthUI === 'function') updateAuthUI(); else console.error("updateAuthUI no definida"); // Llama a la función de auth.js

    // Actualizar año en el footer
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }

    // Para Checkout.html
    if (document.getElementById('checkout-cart-items')) {
        if (typeof displayCheckoutCart === 'function') {
            displayCheckoutCart();
        } else { console.error("Función displayCheckoutCart no definida."); }
    }

    // Para Profile.html
    if (document.getElementById('profile-content')) {
        if (typeof loadProfileContent === 'function') {
            loadProfileContent(); // Llama a la función de profile.js
        } else { console.error("Función loadProfileContent no definida."); }
    }

    // Listener para botón "Proceder al Pago" del sidebar del carrito (si existe)
    const checkoutButtonInSidebar = document.getElementById('checkout-btn');
    if (checkoutButtonInSidebar) {
        checkoutButtonInSidebar.addEventListener('click', (e) => {
            e.preventDefault(); // Prevenir si es un enlace
            window.location.href = 'checkout.html'; // Redirigir a la página de checkout
        });
    }
}); 