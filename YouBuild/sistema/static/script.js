document.addEventListener('DOMContentLoaded', function() {
    // Todo tu código de carrusel aquí.
    const title = document.querySelector('.title');
    const carousel = document.querySelector('.carousel');
    const items = document.querySelectorAll('.carousel-item');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    let currentIndex = 0;
    const totalItems = items.length;
    const transitionTime = 5000; // 5 segundos

    function updateCarousel() {
        if (items.length > 0) {
            const itemWidth = items[0].clientWidth; // Solo obtener si hay elementos
            carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
            updateDots();
        }
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    }

    let autoSlideInterval = setInterval(nextSlide, transitionTime);

    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetAutoSlide();
    });

    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetAutoSlide();
    });

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        autoSlideInterval = setInterval(nextSlide, transitionTime);
    }

    const dotsContainer = document.querySelector('.carousel-dots');

    function createDots() {
        for (let i = 0; i < totalItems; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            dot.addEventListener('click', () => {
                currentIndex = i;
                updateCarousel();
                resetAutoSlide();
            });
            dotsContainer.appendChild(dot);
        }
    }

    function updateDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    createDots();
    updateDots();
    window.addEventListener('resize', updateCarousel);
    window.addEventListener('resize', () => {
        updateCarousel(); // Actualiza el carrusel cuando cambia el tamaño de la ventana
    });
    
});



// Ajusta el carrusel al cambiar el tamaño de la ventana (para mantener la responsividad)


function verDetalles(productId) {
    window.location.href = `/producto/${productId}/`;
}

function volverALista() {
    window.location.href = "/";
}
