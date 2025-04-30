// js/theme.js
const themeToggleButton = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

// Aplica el tema inicial al cargar la página
function initializeTheme() {
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        // Si no hay tema guardado, comprobamos la preferencia del sistema
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        if (prefersDarkScheme.matches && !currentTheme) {
            document.body.classList.add('dark-mode');
            // Opcional: guardar la preferencia del sistema si no había nada antes
            // localStorage.setItem('theme', 'dark');
        } else {
             document.body.classList.remove('dark-mode');
        }
    }
}

// Cambia el tema y guarda la preferencia
function switchTheme() {
    let newTheme = 'light';
    if (!document.body.classList.contains('dark-mode')) {
        document.body.classList.add('dark-mode');
        newTheme = 'dark';
    } else {
        document.body.classList.remove('dark-mode');
        newTheme = 'light';
    }
    localStorage.setItem('theme', newTheme);
}

// Añadir el listener al botón
if (themeToggleButton) {
    themeToggleButton.addEventListener('click', switchTheme);
}

