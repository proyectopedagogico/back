// js/main.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM completamente cargado y parseado.");

    // Inicializar funcionalidades COMUNES a todas las páginas
    initializeTheme();
    loadCart();
    updateAuthUI(); // <- ESTO ACTUALIZA EL BOTÓN LOGIN/PERFIL EN EL NAV

    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }

    // ---- INICIALIZACIÓN ESPECÍFICA DE PÁGINA ----

    // Para Checkout.html
    if (document.getElementById('checkout-cart-items')) {
        if (typeof displayCheckoutCart === 'function') {
            displayCheckoutCart();
        } else { console.error("Función displayCheckoutCart no definida."); }
    }

    // --- NUEVO: Para Profile.html ---
    if (document.getElementById('profile-content')) { // Si existe el contenedor principal del perfil
        if (typeof loadProfileContent === 'function') {
            loadProfileContent(); // Llama a la función de profile.js
        } else { console.error("Función loadProfileContent no definida."); }
    }
    // --- FIN NUEVO ---


    // Listener para botón "Proceder al Pago" del sidebar (si existe)
    const checkoutButtonInSidebar = document.getElementById('checkout-btn');
    if (checkoutButtonInSidebar) {
        checkoutButtonInSidebar.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = 'checkout.html';
        });
    }

});