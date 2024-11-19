document.getElementById('autocompletarBtn').addEventListener('click', function() { 
    fetch('/obtener-direccion/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('departamento').value = data.departamento;
            document.getElementById('provincia').value = data.provincia;
            document.getElementById('municipio').value = data.municipio;
        })
        .catch(error => {
            console.error('Error al autocompletar la dirección:', error);
        });
});

document.getElementById('confirmPurchaseBtn').addEventListener('click', function() {
    const paymentSection = document.getElementById('paymentSection');
    const paymentOption = document.getElementById('payment-option').value;

    if (!paymentOption) {
        alert('Por favor selecciona un método de pago.');
        return;
    }

    // Mostrar la sección de pago y generar el código QR
    paymentSection.classList.remove('hidden');
    generateQRCode();
});

function generateQRCode() {
    const amount = document.getElementById('amount').textContent;
    const transactionId = 'TRANS-' + Math.random().toString(36).substr(2, 9);
    const paymentInfo = {
        amount: amount,
        transactionId: transactionId,
        merchantName: 'Transacción YouBuild'
    };

    const qr = qrcode(0, 'M');
    qr.addData(JSON.stringify(paymentInfo));
    qr.make();
    document.getElementById('qrcode').innerHTML = qr.createImgTag(5, 10, "Código QR de pago");
}

document.getElementById('checkPayment').addEventListener('click', function() {
    const checkPaymentButton = document.getElementById('checkPayment');
    const paymentStatus = document.getElementById('paymentStatus');
    const statusMessage = document.getElementById('statusMessage');

    checkPaymentButton.disabled = true;
    checkPaymentButton.textContent = 'Verificando...';

    setTimeout(() => {
        const isPaid = Math.random() < 0.5;
        paymentStatus.classList.remove('hidden');

        if (isPaid) {
            statusMessage.textContent = '¡Su compra ha sido realizada exitosamente!';
            statusMessage.classList.add('text-green-600');
            statusMessage.classList.remove('text-red-600');

            // Mostrar el recibo
            showReceipt();
        } else {
            statusMessage.textContent = 'Pago no recibido. Por favor, intenta de nuevo.';
            statusMessage.classList.add('text-red-600');
            statusMessage.classList.remove('text-green-600');
        }

        checkPaymentButton.disabled = false;
        checkPaymentButton.textContent = 'Ya realicé el pago';
    }, 2000);
});

// Función para mostrar el recibo
// Función para mostrar el recibo
function showReceipt() {
    const successMessage = document.getElementById('successMessage');
    const orderSummaryBody = document.getElementById('orderSummaryBody');
    const orderTotal = document.getElementById('orderTotal');
    const shippingInfo = document.getElementById('shippingInfo');

    // Limpiar el contenido del recibo antes de llenarlo
    orderSummaryBody.innerHTML = '';

    // Llenar el recibo con los mismos datos que ya están en la tabla de productos
    const productRows = document.querySelectorAll('.confirmacion-carrito-tabla tbody tr');
    productRows.forEach(row => {
        const clonedRow = row.cloneNode(true);  // Clonar la fila para agregarla al recibo
        orderSummaryBody.appendChild(clonedRow);
    });

    // Llenar el total del recibo
    const total = document.querySelector('.confirmacion-total h3:last-of-type').textContent;
    orderTotal.textContent = total;

    // Llenar la dirección de envío en el recibo
    const departamento = document.getElementById('departamento').value;
    const provincia = document.getElementById('provincia').value;
    const municipio = document.getElementById('municipio').value;

    shippingInfo.innerHTML = `<p><strong>Dirección:</strong> ${departamento}, ${provincia}, ${municipio}</p>`;

    // Mostrar el mensaje de éxito con el recibo
    successMessage.classList.remove('hidden');
}
