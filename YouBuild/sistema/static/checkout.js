document.addEventListener('DOMContentLoaded', function() {
    const shippingForm = document.getElementById('shippingForm');
    const paymentSection = document.getElementById('paymentSection');
    const autocompleteBtn = document.getElementById('autocompleteBtn');
    const checkPaymentButton = document.getElementById('checkPayment');
    const paymentStatus = document.getElementById('paymentStatus');
    const statusMessage = document.getElementById('statusMessage');
    const amount = document.getElementById('amount').textContent;

    autocompleteBtn.addEventListener('click', function() {
        document.getElementById('street').value = 'Calle Principal 123';
        document.getElementById('city').value = 'Ciudad Ejemplo';
        document.getElementById('state').value = 'Estado Ejemplo';
    });

    shippingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateForm()) {
            showPaymentSection();
        }
    });

    function validateForm() {
        let isValid = true;
        shippingForm.querySelectorAll('input[required]').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                showError(input, 'Este campo es requerido');
            } else {
                hideError(input);
            }
        });
        return isValid;
    }

    function showError(input, message) {
        const errorElement = input.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('error-message')) {
            const error = document.createElement('p');
            error.classList.add('error-message', 'text-red-500', 'text-sm', 'mt-1');
            error.textContent = message;
            input.parentNode.insertBefore(error, input.nextSibling);
        }
        input.classList.add('border-red-500');
    }

    function hideError(input) {
        const errorElement = input.nextElementSibling;
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.remove();
        }
        input.classList.remove('border-red-500');
    }

    function showPaymentSection() {
        paymentSection.classList.remove('hidden');
        generateQRCode();
        window.scrollTo(0, document.body.scrollHeight);
    }

    function generateQRCode() {
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

    checkPaymentButton.addEventListener('click', checkPaymentStatus);

    function checkPaymentStatus() {
        checkPaymentButton.disabled = true;
        checkPaymentButton.textContent = 'Verificando...';

        setTimeout(() => {
            const isPaid = Math.random() < 0.5; // 50% de probabilidad de éxito
            displayPaymentStatus(isPaid);
            checkPaymentButton.disabled = false;
            checkPaymentButton.textContent = 'Verificar Pago';
        }, 2000);
    }

    function displayPaymentStatus(isPaid) {
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
    }
});
