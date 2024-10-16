document.getElementById('autocompletarBtn').addEventListener('click', function() {
    // Realizamos la petición AJAX para obtener los datos de dirección
    fetch('/obtener-direccion/')
        .then(response => response.json())
        .then(data => {
            // Mantener el nombre completo que ya está cargado en el input del HTML
            // No es necesario actualizar el campo de nombre ya que no cambia.
            
            // Actualizamos los campos con los datos recibidos
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

    // Verificar que se haya seleccionado un método de pago antes de mostrar el QR
    if (!paymentOption) {
        alert('Por favor selecciona un método de pago.');
        return;
    }

    // Hacer visible la sección de pago con QR
    paymentSection.classList.remove('hidden');
    
    // Generar el código QR
    generateQRCode();
});

// Función para generar el código QR
function generateQRCode() {
    const amount = document.getElementById('amount').textContent;
    const transactionId = 'TRANS-' + Math.random().toString(36).substr(2, 9); // Generar un ID de transacción único
    const paymentInfo = {
        amount: amount,
        transactionId: transactionId,
        merchantName: 'Transaccion Youbuild'
    };

    const qr = qrcode(0, 'M');  // Crear la instancia del QR
    qr.addData(JSON.stringify(paymentInfo));  // Agregar los datos de la transacción al QR
    qr.make();  // Generar el QR
    document.getElementById('qrcode').innerHTML = qr.createImgTag(5, 10, "Código QR de pago");  // Insertar el QR en el HTML
}

// Verificar el estado de pago (simulado)
document.getElementById('checkPayment').addEventListener('click', function() {
    const checkPaymentButton = document.getElementById('checkPayment');
    const paymentStatus = document.getElementById('paymentStatus');
    const statusMessage = document.getElementById('statusMessage');

    checkPaymentButton.disabled = true;
    checkPaymentButton.textContent = 'Verificando...';

    // Simulación del estado de pago (esto deberías reemplazarlo con una verificación real si usas un sistema de pagos)
    setTimeout(() => {
        const isPaid = Math.random() < 0.5;  // Simular pago exitoso o fallido aleatoriamente
        paymentStatus.classList.remove('hidden');

        if (isPaid) {
            statusMessage.textContent = '¡Su compra ha sido realizada exitosamente!';
            statusMessage.classList.add('text-green-600');
            statusMessage.classList.remove('text-red-600');
        } else {
            statusMessage.textContent = 'Pago no recibido. Por favor, intenta de nuevo.';
            statusMessage.classList.add('text-red-600');
            statusMessage.classList.remove('text-green-600');
        }

        checkPaymentButton.disabled = false;
        checkPaymentButton.textContent = 'Ya realicé el pago';
    }, 2000);
});