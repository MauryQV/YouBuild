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

    checkPaymentButton.disabled = true;
    checkPaymentButton.textContent = 'Verificando...';

    setTimeout(() => {
        const isPaid = Math.random() < 0.5; 
        paymentStatus.classList.remove('hidden');

        if (isPaid) {
            statusMessage.textContent = '¡Pago exitoso!';
            statusMessage.classList.add('text-green-600');
            statusMessage.classList.remove('text-red-600');
        } else {
            statusMessage.textContent = 'Pago no recibido. Por favor, intenta de nuevo.';
            statusMessage.classList.add('text-red-600');
            statusMessage.classList.remove('text-green-600');
        }

        checkPaymentButton.disabled = false;
        checkPaymentButton.textContent = 'YA REALICE EL PAGO';
    }, 2000);
});