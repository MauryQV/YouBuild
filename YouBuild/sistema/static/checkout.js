// Mostrar la sección de pago con QR
document.getElementById('confirmPurchaseBtn').addEventListener('click', function() {
    const paymentOption = document.getElementById('payment-option').value;
    if (paymentOption === 'bank-transfer') {
        document.getElementById('paymentSection').classList.remove('hidden');
        generateQRCode();
        window.scrollTo(0, document.body.scrollHeight);
    } else {
        alert('Selecciona un método de pago');
    }
});

// Generar el código QR
function generateQRCode() {
    const amount = document.getElementById('amount').textContent;
    const transactionId = 'TRANS-' + Math.random().toString(36).substr(2, 9);
    const paymentInfo = {
        amount: amount,
        transactionId: transactionId,
        merchantName: 'Tienda Ejemplo'
    };

    const qr = qrcode(0, 'M');
    qr.addData(JSON.stringify(paymentInfo));
    qr.make();
    document.getElementById('qrcode').innerHTML = qr.createImgTag(5, 10, "Código QR de pago");
}

// Verificar el estado de pago
document.getElementById('checkPayment').addEventListener('click', function() {
    const checkPaymentButton = document.getElementById('checkPayment');
    const paymentStatus = document.getElementById('paymentStatus');
    const statusMessage = document.getElementById('statusMessage');
    const successMessage = document.getElementById('successMessage');
    const orderDetails = document.getElementById('orderDetails');
    const orderSummaryBody = document.getElementById('orderSummaryBody');
    const shippingDetails = document.getElementById('shippingDetails');
    const orderTotal = document.getElementById('orderTotal');

    checkPaymentButton.disabled = true;
    checkPaymentButton.textContent = 'Verificando...';

    setTimeout(() => {
        const isPaid = Math.random() < 0.5; 
        paymentStatus.classList.remove('hidden');

        if (isPaid) {
            statusMessage.textContent = '¡Pago exitoso!';
            statusMessage.classList.add('text-green-600');
            statusMessage.classList.remove('text-red-600');

            // Mostrar mensaje de éxito con número de pedido y detalles del producto
            const orderId = 'ORD-' + Math.random().toString(36).substr(2, 9);
            orderDetails.innerHTML = `Número de pedido: ${orderId}`;

            // Llenar los detalles del pedido
            const productRows = document.querySelectorAll('.confirmacion-carrito-tabla tbody tr');
            orderSummaryBody.innerHTML = '';
            let totalAmount = 0;
            productRows.forEach(row => {
                const productName = row.cells[0].textContent;
                const productQuantity = row.cells[1].textContent;
                const productPrice = parseFloat(row.cells[2].textContent.replace(' Bs.', ''));
                const productTotal = parseFloat(row.cells[3].textContent.replace(' Bs.', ''));
                totalAmount += productTotal;
                orderSummaryBody.innerHTML += `
                    <tr>
                        <td>${productName}</td>
                        <td>${productQuantity}</td>
                        <td>${productPrice.toFixed(2)} Bs.</td>
                        <td>${productTotal.toFixed(2)} Bs.</td>
                    </tr>
                `;
            });

            // Mostrar el total
            orderTotal.textContent = `${totalAmount.toFixed(2)} Bs.`;

            // Llenar los detalles de la dirección de envío
            const shippingInfo = document.querySelector('.confirmacion-shipping-info');
            shippingDetails.innerHTML = shippingInfo.innerHTML;

            successMessage.classList.remove('hidden');
        } else {
            statusMessage.textContent = 'Pago no recibido. Por favor, intenta de nuevo.';
            statusMessage.classList.add('text-red-600');
            statusMessage.classList.remove('text-green-600');
        }

        checkPaymentButton.disabled = false;
        checkPaymentButton.textContent = 'YA REALICE EL PAGO';
    }, 2000);
});

// Obtener los detalles del producto
function getProductDetails() {
    const productRows = document.querySelectorAll('.confirmacion-carrito-tabla tbody tr');
    let productDetails = '<strong>Detalles del producto:</strong><br>';
    productRows.forEach(row => {
        const productName = row.cells[0].textContent;
        const productQuantity = row.cells[1].textContent;
        const productPrice = row.cells[2].textContent;
        const productTotal = row.cells[3].textContent;
        productDetails += `${productName} - Cantidad: ${productQuantity}, Precio Unitario: ${productPrice}, Total: ${productTotal}<br>`;
    });
    return productDetails;
}