// Variables para el carrusel
const title = document.querySelector('.title');
const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

let currentIndex = 0;
const totalItems = items.length;
const transitionTime = 5000; // 5 segundos

// Función que actualiza el desplazamiento del carrusel
function updateCarousel() {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    updateDots(); 
}

// Función para ir al siguiente slide
function nextSlide() {
    currentIndex = (currentIndex + 1) % totalItems; 
    updateCarousel();
}

// Función para regresar al slide anterior
function prevSlide() {
    currentIndex = (currentIndex - 1 + totalItems) % totalItems;
    updateCarousel();
}

// Función para reiniciar el auto-slide después de interacción del usuario
function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(nextSlide, transitionTime);
}

// Eventos para los botones "prev" y "next"
nextBtn.addEventListener('click', () => {
    nextSlide();
    resetAutoSlide(); // Reinicia el temporizador
});

prevBtn.addEventListener('click', () => {
    prevSlide();
    resetAutoSlide(); // Reinicia el temporizador
});

// Automático: Cambia de imagen cada 5 segundos
let autoSlideInterval = setInterval(nextSlide, transitionTime);

// Control de los puntos de navegación (dots)
const dotsContainer = document.querySelector('.carousel-dots');

function createDots() {
    for (let i = 0; i < totalItems; i++) {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        dot.addEventListener('click', () => {
            currentIndex = i; 
            updateCarousel(); 
            resetAutoSlide(); // Reinicia el temporizador
        });
        dotsContainer.appendChild(dot);
    }
}

// Actualiza los puntos de navegación para reflejar el slide activo
function updateDots() {
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex);
    });
}

// Crea los puntos al iniciar
createDots();
updateDots();

// Ajusta el carrusel al cambiar el tamaño de la ventana (para mantener la responsividad)
window.addEventListener('resize', () => {
    updateCarousel(); // Actualiza el carrusel cuando cambia el tamaño de la ventana
});


function verDetalles(productId) {
    window.location.href = `/producto/${productId}/`;
}

function volverALista() {
    window.location.href = "/";
}
