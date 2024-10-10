let slideIndex = 0;
showSlides(slideIndex);

function showSlides(n) {
    let slides = document.getElementsByClassName("carousel-productos-item");
    let dots = document.getElementsByClassName("dot");
    if (n >= slides.length) { slideIndex = 0 }
    if (n < 0) { slideIndex = slides.length - 1 }
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }
    slides[slideIndex].classList.add("active");
    dots[slideIndex].classList.add("active");
}

function changeSlide(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function volverALista() {
    window.location.href = "/";
}

