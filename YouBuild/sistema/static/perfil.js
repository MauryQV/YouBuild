document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('perfil-form');
    const imageInput = document.getElementById('imagen_perfil');
    const profileIcon = document.querySelector('.profile-icon');

    // Validación de contraseña basada en los requisitos de gestUs.py
    const validatePassword = (password) => {
        const errors = [];
        if (password.length < 8) {
            errors.push("La contraseña debe tener al menos 8 caracteres.");
        }
        if (!/[A-Z]/.test(password)) {
            errors.push("La contraseña debe tener al menos una letra mayúscula.");
        }
        if (!/\d/.test(password)) {
            errors.push("La contraseña debe tener al menos un número.");
        }
        if (!/[!@#$%^&*()]/.test(password)) {
            errors.push("La contraseña debe tener al menos un carácter especial (!@#$%^&*()).");
        }
        return errors;
    };

    // Validación de campos
    const validateField = (input) => {
        const value = input.value.trim();
        const validation = input.dataset.validation;

        if (!validation) return true;

        const rules = validation.split('|');
        let isValid = true;
        let errorMessage = '';

        rules.forEach(rule => {
            switch(rule) {
                case 'required':
                    if (!value) {
                        isValid = false;
                        errorMessage = 'Este campo es requerido';
                    }
                    break;
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        isValid = false;
                        errorMessage = 'Ingrese un correo electrónico válido';
                    }
                    break;
                case 'phone':
                    const phoneRegex = /^\+?[\d\s-]{8,}$/;
                    if (!phoneRegex.test(value)) {
                        isValid = false;
                        errorMessage = 'Ingrese un número de teléfono válido';
                    }
                    break;
                case 'password':
                    const passwordErrors = validatePassword(value);
                    if (passwordErrors.length > 0) {
                        isValid = false;
                        errorMessage = passwordErrors.join(' ');
                    }
                    break;
            }
        });

        const errorElement = input.nextElementSibling;
        if (!isValid) {
            input.classList.add('error');
            errorElement.textContent = errorMessage;
            errorElement.classList.add('visible');
        } else {
            input.classList.remove('error');
            errorElement.classList.remove('visible');
        }

        return isValid;
    };

    // Manejo de imagen de perfil
    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.borderRadius = '50%';
                img.style.objectFit = 'cover';

                profileIcon.innerHTML = '';
                profileIcon.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });

    // Actualización en tiempo real de la información mostrada
    document.getElementById('nombre_completo').addEventListener('input', function(e) {
        document.getElementById('display-nombre').textContent = e.target.value;
    });

    document.getElementById('numero_celular').addEventListener('input', function(e) {
        document.getElementById('display-celular').textContent = e.target.value;
    });

    document.getElementById('correo').addEventListener('input', function(e) {
        document.getElementById('display-correo').textContent = e.target.value;
    });

    // Manejo del cambio de contraseña
    document.getElementById('btn-cambiar-password').addEventListener('click', function() {
        const currentPassword = document.getElementById('password_actual');
        const newPassword = document.getElementById('nueva_contrasena');

        if (!validateField(currentPassword) || !validateField(newPassword)) {
            return;
        }

        // Aquí iría la lógica para cambiar la contraseña
        alert('Contraseña actualizada exitosamente');
        currentPassword.value = '';
        newPassword.value = '';
    });

    // Validación del formulario completo
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        let isValid = true;
        const inputs = form.querySelectorAll('input[data-validation]');

        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            // Aquí iría la lógica para enviar el formulario
            alert('Cambios guardados exitosamente');
        }
    });

    // Validación en tiempo real
    const inputs = form.querySelectorAll('input[data-validation]');
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
    });
});
