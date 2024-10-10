document.querySelectorAll('.quantity-selector').forEach(selector => {
    const decrementButton = selector.querySelector('.decrement');
    const incrementButton = selector.querySelector('.increment');
    const input = selector.querySelector('.quantity-input');

    decrementButton.addEventListener('click', () => {
        let quantity = parseInt(input.value);
        if (quantity > 1) {  // Ajusta este valor mínimo si lo necesitas
            input.value = quantity - 1;
        }
    });

    incrementButton.addEventListener('click', () => {
        let quantity = parseInt(input.value);
        input.value = quantity + 1;
    });
});
