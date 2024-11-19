document.addEventListener('DOMContentLoaded', function() {
    const mainImage = document.getElementById('main-image');
    const imageDots = document.getElementById('image-dots');
    const leftNav = document.querySelector('.image-nav.left');
    const rightNav = document.querySelector('.image-nav.right');
    const countdown = document.getElementById('countdown');
    const buyNowBtn = document.getElementById('buy-now');
    const addToCartBtn = document.getElementById('add-to-cart');
    const addToListBtn = document.getElementById('add-to-list');

    const images = Array.from(imageDots.children).map(dot => dot.dataset.image);
    let currentImageIndex = 0;

    function updateImage() {
        mainImage.src = images[currentImageIndex];
        updateDots();
    }

    function updateDots() {
        Array.from(imageDots.children).forEach((dot, index) => {
            dot.classList.toggle('active', index === currentImageIndex);
        });
    }

    leftNav.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        updateImage();
    });

    rightNav.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        updateImage();
    });

    imageDots.addEventListener('click', (event) => {
        if (event.target.classList.contains('dot')) {
            currentImageIndex = Array.from(imageDots.children).indexOf(event.target);
            updateImage();
        }
    });

    function updateCountdown() {
        const endTime = parseInt(countdown.dataset.endTime) * 1000;
        const now = new Date().getTime();
        const timeLeft = endTime - now;

        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            countdown.innerHTML = "<strong>Oferta finalizada</strong>";
        } else {
            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            countdown.innerHTML = `<strong>${hours}h: ${minutes}m: ${seconds}s</strong>`;
        }
    }

    const countdownInterval = setInterval(updateCountdown, 1000);

    function handleAction(action, productId) {
        return fetch(`/${action}/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            return data;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ha ocurrido un error. Por favor, inténtalo de nuevo.');
        });
    }

    buyNowBtn.addEventListener('click', async () => {
        buyNowBtn.disabled = true;
        await handleAction('buy-now', buyNowBtn.dataset.productId);
        buyNowBtn.disabled = false;
    });

    addToCartBtn.addEventListener('click', async () => {
        addToCartBtn.disabled = true;
        await handleAction('add-to-cart', addToCartBtn.dataset.productId);
        addToCartBtn.disabled = false;
    });

    addToListBtn.addEventListener('click', async () => {
        addToListBtn.disabled = true;
        await handleAction('add-to-wishlist', addToListBtn.dataset.productId);
        addToListBtn.disabled = false;
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize
    updateCountdown();
});