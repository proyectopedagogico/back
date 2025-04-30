function validarDNI(dniInput) {
    const dni = dniInput.toUpperCase();
    const tablaLetras = "TRWAGMYFPDXBNJZSQVHLCKE";

    if (!/^[0-9]{8}[A-Z]$/.test(dni)) return null; // Formato inválido

    const numeroStr = dni.substring(0, 8);
    const letraProporcionada = dni.charAt(8);
    const numero = parseInt(numeroStr, 10);

    if (isNaN(numero)) return null; // Error conversión número

    const letraCalculada = tablaLetras.charAt(numero % 23);

    return (letraCalculada === letraProporcionada) ? true : letraCalculada;
}

// --- EVENT LISTENERS ---
function addProfileEventListeners(profileContainer) {
    // Buscar elementos *dentro* del contenedor del perfil para eficiencia
    const logoutButton = profileContainer.querySelector('#logout-button-profile');
    const validateDniButton = profileContainer.querySelector('#validate-dni-btn');
    const dniInput = profileContainer.querySelector('#dni-input');
    const dniMessageElement = profileContainer.querySelector('#dni-validation-message');
    const profilePicInput = profileContainer.querySelector('#profile-pic-input');
    const profilePic = profileContainer.querySelector('#profile-pic'); // La <img>

    // Listener Botón Cerrar Sesión
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            if (typeof logout === 'function') {
                logout();
                window.location.href = 'index.html';
            } else {
                console.error("Función logout() no definida.");
                alert("Error al cerrar sesión.");
            }
        });
    }

    // Listener Botón Validar DNI
    if (validateDniButton && dniInput && dniMessageElement) {
        validateDniButton.addEventListener('click', () => {
            const dniValue = dniInput.value.trim();
            dniMessageElement.textContent = "";
            dniMessageElement.classList.remove('valid', 'invalid');

            if (!dniValue) {
                dniMessageElement.textContent = "Por favor, introduce un DNI.";
                dniMessageElement.classList.add('invalid');
                return;
            }

            const validationResult = validarDNI(dniValue);

            if (validationResult === true) {
                dniMessageElement.textContent = "DNI válido.";
                dniMessageElement.classList.add('valid');
            } else if (validationResult === null) {
                dniMessageElement.textContent = "Formato de DNI inválido (8 números y 1 letra).";
                dniMessageElement.classList.add('invalid');
            } else {
                dniMessageElement.textContent = `Letra incorrecta. La letra correcta para ${dniValue.substring(0,8)} es '${validationResult}'.`;
                dniMessageElement.classList.add('invalid');
            }
        });
    }

    // Listener Input para cambiar foto de perfil
    if (profilePicInput && profilePic) {
        profilePicInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const imageDataUrl = e.target.result;
                    profilePic.src = imageDataUrl;
                    try {
                        localStorage.setItem('userProfilePic', imageDataUrl);
                        console.log("Foto de perfil actualizada (simulación localStorage).");
                    } catch (storageError) {
                        console.error("Error al guardar imagen en localStorage:", storageError);
                        alert("No se pudo guardar la nueva imagen de perfil.");
                    }
                }
                reader.readAsDataURL(file);
            } else if (file) {
                alert("Por favor, selecciona un archivo de imagen válido.");
            }
        });
    }
}


// --- FUNCIÓN PRINCIPAL ---
// Función principal para cargar y manejar la página de perfil
function loadProfileContent() {
    // 1. Verificar si el usuario está logueado
    if (typeof isLoggedIn !== 'function' || !isLoggedIn()) {
        console.warn("Usuario no logueado. Redirigiendo...");
        window.location.href = 'index.html';
        return;
    }

    // 2. Obtener elementos principales del DOM
    const profileContentContainer = document.getElementById('profile-content');
    const loadingMessage = document.getElementById('profile-loading-message');
    const profileTemplate = document.getElementById('profile-template');

    if (!profileContentContainer || !loadingMessage || !profileTemplate) {
        console.error("Error: Faltan elementos base del DOM en profile.html.");
        if(loadingMessage) loadingMessage.textContent = "Error al cargar perfil.";
        return;
    }

    // 3. Clonar y preparar contenido de la plantilla
    loadingMessage.remove();
    const templateNode = profileTemplate.content.cloneNode(true); // Clonamos el nodo del template

    // 4. Poblar datos del usuario en el nodo clonado
    const emailElement = templateNode.querySelector('#profile-email'); // Usamos querySelector en el nodo clonado
    const profilePicElement = templateNode.querySelector('#profile-pic');
    const userEmail = sessionStorage.getItem('userEmail');

    if (emailElement && userEmail) {
        emailElement.textContent = userEmail;
    } else if (emailElement) {
        emailElement.textContent = "Email no encontrado";
    }

    const savedPic = localStorage.getItem('userProfilePic');
    if (profilePicElement && savedPic) {
        profilePicElement.src = savedPic;
    }

    // 5. Añadir el nodo clonado y poblado al contenedor principal
    profileContentContainer.innerHTML = ''; // Limpiar por si acaso
    profileContentContainer.appendChild(templateNode); // Añadimos el contenido clonado

    // 6. Añadir Event Listeners AHORA que los elementos están en el DOM
    // Pasamos el contenedor donde acabamos de añadir los elementos
    addProfileEventListeners(profileContentContainer);
}