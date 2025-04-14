// js/cart.js - VERSIÓN DEL USUARIO CON ROBUSTEZ AÑADIDA

let cart = [];
// Obtener referencias a elementos (pueden ser null si no existen en la página)
const cartButton = document.getElementById('cart-button');
const cartSidebar = document.getElementById('cart-sidebar');
const closeCartButton = document.getElementById('close-cart-btn');
const cartItemsContainer = document.getElementById('cart-items-container');
const cartCountElement = document.getElementById('cart-count');
const cartTotalElement = document.getElementById('cart-total');
const productListContainer = document.getElementById('product-list'); // Para delegación de eventos
const overlay = document.getElementById('overlay');

// Carga el carrito desde localStorage
function loadCart() {
    const storedCart = localStorage.getItem('shoppingCart');
    cart = storedCart ? JSON.parse(storedCart) : [];
    renderCart(); // Renderizar intentará actualizar UI si los elementos existen
}

// Guarda el carrito en localStorage
function saveCart() {
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
}

// Renderiza el contenido del carrito en la UI - AHORA CON COMPROBACIONES
function renderCart() {
    // Solo intentar renderizar items si el contenedor existe
    if (cartItemsContainer) {
        cartItemsContainer.innerHTML = ''; // Limpiar items actuales
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p>Tu carrito está vacío.</p>';
        } else {
            cart.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('cart-item');
                const imageUrl = item.image && typeof item.image === 'string' ? item.image : 'https://via.placeholder.com/60?text=No+Img';
                itemElement.innerHTML = `
                    <img src="${imageUrl}" alt="${item.name || ''}" class="cart-item-image">
                    <div class="cart-item-details">
                        <h4 class="cart-item-title">${item.name || 'Nombre no disponible'}</h4>
                        <p class="cart-item-price">€${(item.price || 0).toFixed(2)}</p>
                        <div class="cart-item-quantity">
                            <button class="quantity-btn decrease-qty" data-id="${item.id}" aria-label="Disminuir cantidad">-</button>
                            <span>${item.quantity || 0}</span>
                            <button class="quantity-btn increase-qty" data-id="${item.id}" aria-label="Aumentar cantidad">+</button>
                        </div>
                    </div>
                    <button class="cart-item-remove-btn" data-id="${item.id}" aria-label="Eliminar item">&times;</button>
                `;
                cartItemsContainer.appendChild(itemElement);
            });
        }
    }
    // else { console.log("Debug: Contenedor de items del carrito no encontrado en esta página."); } // Descomentar para depurar

    // Calcular totales independientemente de si se renderizaron items
    let total = 0;
    let count = 0;
    cart.forEach(item => {
        total += (item.price || 0) * (item.quantity || 0);
        count += (item.quantity || 0);
    });

    // Actualizar contador y total SOLO si los elementos existen
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
    if (cartTotalElement) {
        cartTotalElement.textContent = total.toFixed(2);
    }

    updateCartButtonActiveState(); // Marcar botón si hay items (también verifica si el botón existe)
}

// Añade un producto al carrito
function addToCart(product) {
     if (!product || !product.id || !product.name || typeof product.price === 'undefined') {
        console.error("Intento de añadir producto inválido:", product);
        return;
     }
    const existingItemIndex = cart.findIndex(item => item.id === product.id);
    if (existingItemIndex > -1) {
        cart[existingItemIndex].quantity = (cart[existingItemIndex].quantity || 0) + 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    saveCart();
    renderCart();
    // Solo intenta mostrar el sidebar si existe
    if (cartSidebar) {
       showCartSidebar();
    }
}

// Actualiza la cantidad de un item
function updateQuantity(productId, change) {
    if (!productId) return;
    const itemIndex = cart.findIndex(item => item.id === productId);
    if (itemIndex > -1) {
        cart[itemIndex].quantity = (cart[itemIndex].quantity || 0) + change;
        if (cart[itemIndex].quantity <= 0) {
            cart.splice(itemIndex, 1);
        }
        saveCart();
        renderCart(); // Renderizar actualiza UI si existe
    }
}

// Elimina un item del carrito
function removeFromCart(productId) {
    if (!productId) return;
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    renderCart(); // Renderizar actualiza UI si existe
}

// Muestra/Oculta el sidebar del carrito - CON LOGS Y COMPROBACIONES
function toggleCartSidebar() {
    // Verificar si los elementos existen antes de usarlos
    if (!cartSidebar || !overlay) {
        console.error("Error al alternar: No se encontraron los elementos sidebar u overlay.");
        return;
    }

    // Ver estado ANTES del cambio (LOGS DE DEPURACIÓN - PUEDES BORRARLOS LUEGO)
    const sidebarRightBefore = window.getComputedStyle(cartSidebar).right;
    const sidebarClassesBefore = cartSidebar.className;
    const overlayClassesBefore = overlay.className;
    console.log(
        "Antes - Right:", sidebarRightBefore,
        "Sidebar Classes:", sidebarClassesBefore,
        "Overlay Classes:", overlayClassesBefore
    );

    cartSidebar.classList.toggle('visible');
    overlay.classList.toggle('hidden', !cartSidebar.classList.contains('visible'));

    // Ver estado DESPUÉS del cambio (LOGS DE DEPURACIÓN - PUEDES BORRARLOS LUEGO)
    setTimeout(() => {
        const sidebarRightAfter = window.getComputedStyle(cartSidebar).right;
        const sidebarClassesAfter = cartSidebar.className;
        const overlayClassesAfter = overlay.className;
        console.log(
            "Después - Right:", sidebarRightAfter,
            "Sidebar Classes:", sidebarClassesAfter,
            "Overlay Classes:", overlayClassesAfter
        );
    }, 0);
}

// Muestra explícitamente el sidebar
function showCartSidebar() {
    if (!cartSidebar || !overlay) {
         // Comentado para no llenar la consola si no existe
         // console.error("Error al mostrar: No se encontraron los elementos sidebar u overlay.");
         return;
    }
    cartSidebar.classList.add('visible');
    overlay.classList.remove('hidden');
    // console.log("showCartSidebar ejecutado. Overlay hidden:", overlay.classList.contains('hidden')); // Log opcional
}

// Oculta explícitamente el sidebar
function hideCartSidebar() {
     if (!cartSidebar || !overlay) {
         // console.error("Error al ocultar: No se encontraron los elementos sidebar u overlay.");
         return;
     }
     // console.log("Intentando ocultar sidebar y añadir 'hidden' a overlay"); // Log opcional
    cartSidebar.classList.remove('visible');
    overlay.classList.add('hidden');
    // console.log("Clases del overlay después de ocultar:", overlay.classList); // Log opcional
}

// Marca el botón del carrito si hay items
function updateCartButtonActiveState() {
    if (!cartButton) return; // Salir si no hay botón de carrito en esta página
    if (cart.length > 0) {
        cartButton.style.fontWeight = 'bold';
    } else {
        cartButton.style.fontWeight = 'normal';
    }
}

// --- Event Listeners (AHORA CON COMPROBACIONES) ---

if (cartButton) {
    cartButton.addEventListener('click', (e) => {
        e.preventDefault();
        // console.log("Listener del botón del carrito activado"); // Log opcional
        toggleCartSidebar();
    });
}
// else { console.log("Debug: Botón del carrito (#cart-button) no encontrado."); } // Descomentar para depurar

if (closeCartButton) {
    closeCartButton.addEventListener('click', hideCartSidebar);
}
// else { console.log("Debug: Botón cerrar carrito (#close-cart-btn) no encontrado."); } // Descomentar para depurar

if (overlay) {
    overlay.addEventListener('click', () => {
        // console.log("Overlay click detectado"); // Log opcional
        // Solo intentar ocultar sidebar si existe y está visible
        if (cartSidebar && cartSidebar.classList.contains('visible')) {
           hideCartSidebar();
        }
        // Ocultar modal de login si existe y está visible
        const loginModal = document.getElementById('login-modal');
         if (loginModal && !loginModal.classList.contains('hidden') && typeof hideLoginModal === 'function') {
              hideLoginModal();
         }
    });
}
// else { console.log("Debug: Overlay no encontrado."); } // Descomentar para depurar

// Delegación de eventos para botones dentro del carrito
if (cartItemsContainer) {
    cartItemsContainer.addEventListener('click', (event) => {
        const target = event.target;
        const decreaseButton = target.closest('.decrease-qty');
        const increaseButton = target.closest('.increase-qty');
        const removeButton = target.closest('.cart-item-remove-btn');

        if (decreaseButton) { updateQuantity(decreaseButton.dataset.id, -1); }
        else if (increaseButton) { updateQuantity(increaseButton.dataset.id, 1); }
        else if (removeButton) { removeFromCart(removeButton.dataset.id); }
    });
}
// else { console.log("Debug: Contenedor de items del carrito (#cart-items-container) no encontrado."); } // Descomentar para depurar

// Delegación de eventos para botones "Añadir al carrito" en la lista de productos
if (productListContainer) {
    productListContainer.addEventListener('click', (event) => {
        const addButton = event.target.closest('.add-to-cart-btn');
        if (addButton) {
            const card = addButton.closest('.product-card');
            if (card) {
                const nameElement = card.querySelector('.product-title');
                const priceElement = card.querySelector('.price-value');
                const imageElement = card.querySelector('.product-image');
                const product = {
                    id: card.dataset.productId,
                    name: nameElement ? nameElement.textContent : 'Producto Desconocido',
                    price: priceElement ? parseFloat(priceElement.textContent) : 0,
                    image: imageElement ? imageElement.src : 'https://via.placeholder.com/60?text=No+Img'
                };
                // console.log("Listener 'Añadir al carrito' activado para producto:", product); // Log opcional
                addToCart(product);
            }
        }
    });
}
// else { console.log("Debug: Lista de productos (#product-list) no encontrada."); } // Descomentar para depurar

// La llamada a loadCart() se hace desde js/main.js dentro de DOMContentLoaded