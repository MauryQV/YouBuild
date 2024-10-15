document.addEventListener('DOMContentLoaded', function() {
    const updateCart = (itemId, quantity) => {
        fetch(`/update_cart_quantity/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ item_id: itemId, quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`subtotal-${itemId}`).innerText = `Bs ${data.new_subtotal}`;
                document.getElementById(`total`).innerText = `Bs ${data.new_total}`;
            } else {
                alert(data.message);
            }
        });
    };

    document.querySelectorAll('.quantity-btn.increment').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const itemId = input.dataset.itemId;
            let quantity = parseInt(input.value);

            if (quantity < parseInt(input.dataset.stock)) {
                input.value = quantity + 1;
                updateCart(itemId, quantity + 1);
            } else {
                alert("No hay más unidades disponibles de este producto.");
            }
        });
    });

    document.querySelectorAll('.quantity-btn.decrement').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.nextElementSibling;
            const itemId = input.dataset.itemId;
            let quantity = parseInt(input.value);

            if (quantity > 1) {
                input.value = quantity - 1;
                updateCart(itemId, quantity - 1);
            } else {
                if (confirm("¿Deseas eliminar este producto del carrito?")) {
                    updateCart(itemId, 0);
                }
            }
        });
    });
});
