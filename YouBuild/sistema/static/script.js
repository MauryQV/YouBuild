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
    const itemWidth = items[0].clientWidth; // Obtener el ancho actual del ítem
    carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`; // Usar el ancho dinámico
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

function agregarAlCarrito(productId) {
    fetch(`/agregar-al-carrito/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Producto agregado correctamente al carrito');
        } else {
            alert(data.message || 'Error al agregar al carrito');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function agregarAlCarrito(productId) {
    // Usamos fetch para enviar la solicitud POST al servidor
    fetch(`/agregar-al-carrito/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  // Añadir el CSRF token para la protección
        },
        body: JSON.stringify({})  // Cuerpo vacío ya que no necesitamos pasar datos adicionales
    })
    .then(response => {
        if (response.redirected) {
            // Si la respuesta tiene redirección, el carrito fue actualizado correctamente
            window.location.href = response.url;  // Redirigir a la página de carrito o la página original
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.success) {
            // Si la respuesta JSON indica éxito, mostrar un mensaje
            alert(data.message || 'Producto agregado correctamente al carrito');
        } else if (data && data.message) {
            // En caso de error, mostrar el mensaje de error
            alert(data.message || 'Error al agregar el producto al carrito');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al agregar al carrito');
    });
  }

  function registrarse() {
    window.location.href = "/registro";
}