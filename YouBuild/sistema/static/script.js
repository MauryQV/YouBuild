const title = document.querySelector('.title');
const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

let currentIndex = 0;
const totalItems = items.length;
const transitionTime = 5000; // 5 segundos

function updateCarousel() {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    updateDots(); 
}
function nextSlide() {
    currentIndex = (currentIndex + 1) % totalItems; 
    updateCarousel();
}

// Función para regresar al slide anterior
function prevSlide() {
    currentIndex = (currentIndex - 1 + totalItems) % totalItems; // Regresa al índice anterior y reinicia si llega al inicio
    updateCarousel();
}

// Reinicia el temporizador al presionar los botones
function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(nextSlide, transitionTime);
}

// Listeners para los botones
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

const dotsContainer = document.querySelector('.carousel-dots'); // Selecciona el contenedor de puntos

function createDots() {
    for (let i = 0; i < totalItems; i++) {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        dot.addEventListener('click', () => {
            currentIndex = i; // Actualiza el índice actual al hacer clic en el punto
            updateCarousel(); // Actualiza el carrusel
            resetAutoSlide(); // Reinicia el temporizador
        });
        dotsContainer.appendChild(dot);
    }
}

function updateDots() {
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex); // Activa el punto correspondiente
    });
}

createDots();
updateDots(); 

function verDetalles(productId) {
    window.location.href = `/producto/${productId}/`;
}

function volverALista() {
    window.location.href = "/";
}

