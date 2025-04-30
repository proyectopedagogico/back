const authButton = document.getElementById('auth-button');
const overlayForAuth = document.getElementById('overlay'); // Usado por login y carrito

// --- Elementos del Modal de Login ---
const loginModal = document.getElementById('login-modal');
const closeLoginButton = document.getElementById('close-login-btn');
const loginForm = document.getElementById('login-form');
const loginErrorElement = document.getElementById('login-error');
const emailInput = document.getElementById('email'); // Seleccionar aquí si se usa en login()
const passwordInput = document.getElementById('password');
const togglePasswordButton = document.getElementById('togglePassword');

// --- Lógica Toggle Contraseña ---
if (togglePasswordButton && passwordInput) {
    togglePasswordButton.addEventListener('click', function() {
        const currentType = passwordInput.getAttribute('type');
        const newType = currentType === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', newType);
        // Cambia el icono/texto del botón
        this.textContent = newType === 'password' ? '👁️' : '🙈';
    });
} else {
    // Advertir solo si el modal de login existe en la página
    if (loginModal) {
        console.warn("Input de contraseña o botón toggle no encontrados en la página de login.");
    }
}

// --- Funciones de Autenticación ---

// Comprueba si el usuario está logueado
function isLoggedIn() {
    return sessionStorage.getItem('userLoggedIn') === 'true';
}

// Actualiza la UI (botón nav y listeners) basada en el estado de login
function updateAuthUI() {
    // Re-seleccionar authButton aquí o usar la constante global.
    // Si auth.js pudiera cargarse en páginas sin #auth-button, la selección aquí con check es más segura.
    const navAuthButton = document.getElementById('auth-button');
    if (!navAuthButton) {
        // console.log("Botón de autenticación no encontrado en esta página."); // Log opcional
        return; // Salir si el botón no existe
    }

    // Limpiar listeners anteriores para evitar duplicados
    navAuthButton.removeEventListener('click', showLoginModal);
    navAuthButton.removeEventListener('click', logout); // Quitar listener de logout por si acaso

    if (isLoggedIn()) {
        const userEmail = sessionStorage.getItem('userEmail') || 'Usuario';
        navAuthButton.textContent = `Hola, ${userEmail.split('@')[0]}`;
        navAuthButton.classList.remove('btn-secondary');
        navAuthButton.classList.add('btn-success');
        navAuthButton.href = 'profile.html'; // Enlace a perfil
        // No se añade ningún listener de click aquí, la navegación la hace el href
    } else {
        navAuthButton.textContent = 'Login';
        navAuthButton.classList.remove('btn-success');
        navAuthButton.classList.add('btn-secondary');
        navAuthButton.href = '#'; // Para prevenir navegación y activar JS
        navAuthButton.addEventListener('click', showLoginModal); // Listener para abrir modal
    }
}

// Muestra el modal de login
function showLoginModal(event) {
    if (event) event.preventDefault(); // Prevenir comportamiento de enlace '#'
    // Asegurarse que los elementos existen antes de usarlos
    if (loginModal && overlayForAuth && loginErrorElement) {
        loginModal.classList.remove('hidden');
        overlayForAuth.classList.remove('hidden');
        loginErrorElement.classList.add('hidden'); // Ocultar errores previos al mostrar
    } else {
        console.error("No se pueden mostrar el modal de login, faltan elementos (modal, overlay o error msg).");
    }
}

// Oculta el modal de login
function hideLoginModal() {
    if (loginModal && overlayForAuth) {
        loginModal.classList.add('hidden');
        overlayForAuth.classList.add('hidden');
    }
}

// Simula el proceso de login
function login(event) {
    if (event) event.preventDefault(); // Evita el envío real del formulario

    // Validar que los elementos del formulario existen
    if (!emailInput || !passwordInput || !loginErrorElement) {
         console.error("Elementos del formulario de login no encontrados.");
         return;
    }
    const email = emailInput.value;
    const password = passwordInput.value;

    // Simulación básica (en real, llamada a API)
    if (email && password && email.includes('@')) { // Validación mínima
        sessionStorage.setItem('userLoggedIn', 'true');
        sessionStorage.setItem('userEmail', email);
        updateAuthUI(); // Actualizar botón nav
        hideLoginModal(); // Ocultar modal
        // Limpiar campos (opcional pero buena práctica)
        if(loginForm) loginForm.reset(); // Forma más simple de limpiar
        // loginErrorElement.classList.add('hidden'); // hideLoginModal ya lo oculta al principio
    } else {
        loginErrorElement.classList.remove('hidden'); // Mostrar error
        console.error("Intento de login fallido (simulación)");
    }
}

// Realiza el logout
function logout(event) {
    // No necesitamos preventDefault aquí si se llama desde el botón en profile.js
    // Pero si se llamara desde un enlace <a href="#">, sí sería útil.
    // if(event) event.preventDefault();
    sessionStorage.removeItem('userLoggedIn');
    sessionStorage.removeItem('userEmail');
    updateAuthUI(); // Actualizar botón nav
    console.log("Usuario deslogueado");
    // Considerar redirigir a inicio si se hace logout desde una página protegida
    // if (window.location.pathname.includes('profile.html')) {
    //     window.location.href = 'index.html';
    // }
}

// --- Event Listeners (Configuración inicial) ---

// Listener para cerrar modal de login (si existe el botón)
if (closeLoginButton) {
    closeLoginButton.addEventListener('click', hideLoginModal);
}

// Listener para el envío del formulario de login (si existe)
if (loginForm) {
    loginForm.addEventListener('submit', login);
}
