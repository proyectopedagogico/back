// js/auth.js
const authButton = document.getElementById('auth-button');
const loginModal = document.getElementById('login-modal');
const closeLoginButton = document.getElementById('close-login-btn');
const loginForm = document.getElementById('login-form');
const loginErrorElement = document.getElementById('login-error');
const overlayForAuth = document.getElementById('overlay'); // Usamos el mismo overlay

// Comprueba si el usuario está logueado (usando sessionStorage)
function isLoggedIn() {
    return sessionStorage.getItem('userLoggedIn') === 'true';
}

// Actualiza la UI basada en el estado de login
function updateAuthUI() {
    if (isLoggedIn()) {
        const userEmail = sessionStorage.getItem('userEmail') || 'Usuario';
        authButton.textContent = `Hola, ${userEmail.split('@')[0]}`; // Mostrar parte del email
        authButton.classList.remove('btn-secondary');
        authButton.classList.add('btn-success'); // Cambiar estilo a 'logueado'
        authButton.removeEventListener('click', showLoginModal); // Quitar listener de abrir modal
        authButton.addEventListener('click', logout); // Añadir listener de logout
        authButton.href = '#'; // Evitar que navegue si era un enlace
    } else {
        authButton.textContent = 'Login';
        authButton.classList.remove('btn-success');
        authButton.classList.add('btn-secondary'); // Estilo por defecto
        authButton.removeEventListener('click', logout); // Quitar listener de logout
        authButton.addEventListener('click', showLoginModal); // Añadir listener de abrir modal
        authButton.href = '#'; // Asegurarse que no navega
    }
}

// Muestra el modal de login
function showLoginModal(event) {
    if(event) event.preventDefault(); // Prevenir comportamiento del enlace si se hace clic
    loginModal.classList.remove('hidden');
    overlayForAuth.classList.remove('hidden');
    loginErrorElement.classList.add('hidden'); // Ocultar errores previos
}

// Oculta el modal de login
function hideLoginModal() {
    loginModal.classList.add('hidden');
    overlayForAuth.classList.add('hidden');
}

// Simula el proceso de login
function login(event) {
    event.preventDefault(); // Evita el envío real del formulario
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const email = emailInput.value;
    const password = passwordInput.value;

    // --- SIMULACIÓN MUY BÁSICA ---
    // En una aplicación real, esto sería una llamada a un backend (API)
    if (email && password && email.includes('@')) { // Validación mínima
        // Supongamos que el login es exitoso
        sessionStorage.setItem('userLoggedIn', 'true');
        sessionStorage.setItem('userEmail', email);
        updateAuthUI();
        hideLoginModal();
        emailInput.value = ''; // Limpiar campos
        passwordInput.value = '';
        loginErrorElement.classList.add('hidden');
    } else {
        // Mostrar error
        loginErrorElement.classList.remove('hidden');
        console.error("Intento de login fallido (simulación)");
    }
}

// Realiza el logout
function logout(event) {
     if(event) event.preventDefault(); // Si se hace clic en el botón que ahora es de logout
    sessionStorage.removeItem('userLoggedIn');
    sessionStorage.removeItem('userEmail');
    updateAuthUI();
    console.log("Usuario deslogueado");
}

// --- Event Listeners ---

// Cerrar modal de login
if (closeLoginButton) {
    closeLoginButton.addEventListener('click', hideLoginModal);
}

// Listener para el envío del formulario de login
if (loginForm) {
    loginForm.addEventListener('submit', login);
}

// Listener inicial para el botón de Auth (se actualiza en updateAuthUI)
if (authButton) {
    if (!isLoggedIn()) {
        authButton.addEventListener('click', showLoginModal);
    } else {
        authButton.addEventListener('click', logout);
    }
}

// Inicializar la UI de autenticación al cargar (podría ir en main.js)
// updateAuthUI();