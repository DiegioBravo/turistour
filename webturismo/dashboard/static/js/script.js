// Obtener elementos del DOM
const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");
const showPopupBtn = document.querySelector(".login-btn");
const formPopup = document.querySelector(".form-popup");
const hidePopupBtn = formPopup.querySelector(".close-btn");
const signupLoginLink = formPopup.querySelectorAll(".bottom-link a");

// Asegurar que el popup nunca quede activado al cargar la página
document.body.classList.remove("show-popup");

// Mostrar menú móvil
hamburgerBtn.addEventListener("click", () => {
    navbarMenu.classList.toggle("show-menu");
});

// Ocultar menú móvil
hideMenuBtn.addEventListener("click", () => hamburgerBtn.click());

// Mostrar popup de login
showPopupBtn.addEventListener("click", () => {
    document.body.classList.add("show-popup");
});

// Ocultar popup de login
hidePopupBtn.addEventListener("click", () => {
    document.body.classList.remove("show-popup");
});

// Cambiar entre login y signup
signupLoginLink.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        if (link.id === 'signup-link') {
            formPopup.classList.add("show-signup");
        } else {
            formPopup.classList.remove("show-signup");
        }
    });
});
