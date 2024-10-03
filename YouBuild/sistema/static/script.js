const title = document.querySelector('.title');
const text = title.textContent;
title.textContent = '';

// Crea un span para cada letra del título
for (let i = 0; i < text.length; i++) {
    const span = document.createElement('span');
    span.textContent = text[i];
    span.style.opacity = '1'; // Opacidad inicial completamente visible
    span.style.transform = 'scale(1)'; // Tamaño inicial normal
    title.appendChild(span);
}

// Efecto de ola
const spans = title.querySelectorAll('span');

function waveEffect() {
    spans.forEach((span, index) => {
        const delay = index * 100; // Tiempo de retardo por letra
        setTimeout(() => {
            span.style.transform = 'scale(0.75)'; // Aumenta el tamaño de la letra
        }, delay);
        
        // Decrecer después de un tiempo
        setTimeout(() => {
            span.style.transform = 'scale(1)'; // Restaura el tamaño original
        }, delay + 800); // Tiempo después de crecer
    });
}

// Ejecuta el efecto en cadena
function startWaveEffect() {
    waveEffect();
    setTimeout(() => {
        // Después del efecto y la pausa de 1 segundo, vuelve a ejecutar
        startWaveEffect();
    }, (spans.length * 100) + 800 + 5000); // Duración del efecto + pausa de 1 segundo
}

// Comienza el efecto de onda
startWaveEffect();

const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

let currentIndex = 0;
const totalItems = items.length;
const transitionTime = 5000; // 5 segundos

// Función para actualizar la posición del carrusel
function updateCarousel() {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    updateDots(); // Asegúrate de actualizar los puntos cada vez que cambie el carrusel
}

// Función para pasar al siguiente slide
function nextSlide() {
    currentIndex = (currentIndex + 1) % totalItems; // Avanza al siguiente índice y reinicia si llega al final
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

// Crear puntos de navegación
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

// Función para actualizar los puntos
function updateDots() {
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex); // Activa el punto correspondiente
    });
}

// Inicializa los puntos de navegación
createDots();
updateDots(); // Asegúrate de que el punto correcto esté activo al inicio

function verDetalles(productId) {
    window.location.href = `/producto/${productId}/`;
}

function volverALista() {
    window.location.href = "/";
}
