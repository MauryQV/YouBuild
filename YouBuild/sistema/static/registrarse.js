let currentSection = 1;
const totalSections = 3;

const form = document.getElementById('registro-form');
const progressBar = document.getElementById('progress-bar');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');

const provincias = {
    "La Paz": ['Murillo', 'Los Andes', 'Ingavi'],
    "Cochabamba": ['Cercado', 'Vallegrande', 'Chapare'],
    "Santa Cruz": ['Andrés Ibáñez', 'Chiquitos', 'Warnes'],
    "Tarija": ['Cercado', 'Gran Chaco', 'Burdet O´Connor'],
    "Chuquisaca": ['Sucre', 'Oropeza', 'Zudañez'],
    "Potosí": ['Potosí', 'Cinti', 'Tomás Frías'],
    "Oruro": ['Oruro', 'Sajama', 'Poopó'],
    "Beni": ['Cercado', 'Mamoré', 'Yacuma'],
    "Pando": ['Cobija', 'Nicolás Suárez', 'Federico Román']
};

const municipios = {
    "La Paz": ['La Paz', 

'El Alto'],
    "Cochabamba": ['Cochabamba', 'Sacaba'],
    "Santa Cruz": ['Santa Cruz de la Sierra', 'Cotoca'],
    "Tarija": ['Tarija', 'Villazón'],
    "Chuquisaca": ['Sucre', 'Yotala'],
    "Potosí": ['Potosí', 'Uyuni'],
    "Oruro": ['Oruro', 'Huanuni'],
    "Beni": ['Trinidad', 'Riberalta'],
    "Pando": ['Cobija', 'Porvenir']
};

function updateProgressBar() {
    const progress = 33 + ((currentSection - 1) / (totalSections - 1)) * 67;
    progressBar.style.width = `${progress}%`;
}

function showSection(sectionNumber) {
    document.querySelectorAll('.form-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`section${sectionNumber}`).classList.add('active');

    if (sectionNumber === 1) {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    } else if (sectionNumber === totalSections) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'block';
    } else {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    }

    updateProgressBar();
}

function validateField(field) {
    const value = field.value.trim();
    const name = field.name;
    const errorElement = document.getElementById(`error-${name}`);
    let error = '';

    switch (name) {
        case 'nombreCompleto':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (value.length < 4) {
                error = 'Mínimo 4 caracteres';
            } else if (value.length > 50) {
                error = 'Máximo 50 caracteres';
            } else if (/[^a-zA-Z\s]/.test(value)) {
                error = 'El nombre solo puede contener letras';
            } else if ((value.match(/\s/g) || []).length > 7) {
                error = 'Número máximo de espacios 7';
            } else if (/\s{2,}/.test(value)) {
                error = 'No se permiten más de 2 espacios seguidos';
            }
            break;
        case 'nombreUsuario':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (value.length < 5) {
                error = 'Mínimo 5 caracteres';
            } else if (value.length > 15) {
                error = 'Máximo 15 caracteres';
            } else if (/[^a-zA-Z0-9@]/.test(value)) {
                error = 'El nombre de usuario solo puede contener letras y números';
            } else if (/\s/.test(value)) {
                error = 'No se permiten espacios';
            }
            break;
        case 'contrasena':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (value.length < 8) {
                error = 'Mínimo 8 caracteres';
            } else if (value.length > 16) {
                error = 'Límite de caracteres excedido (16)';
            } else if (!/^(?=.*[A-Z])(?=.*\d)(?=.*[ª!"·$%&/()=?¿]).*$/.test(value)) {
                error = 'La contraseña debe tener al menos una letra mayúscula, un número y un carácter especial (ª!"·$%&/()=?¿)';
            }
            break;
        case 'confirmarContrasena':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (value !== document.getElementById('contrasena').value) {
                error = 'Las contraseñas no coinciden';
            }
            break;
        case 'departamento':
        case 'provincia':
        case 'municipio':
            if (!value) {
                error = 'Campo obligatorio';
            }
            break;
        case 'direccion':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (value.length < 10) {
                error = 'Mínimo 10 caracteres';
            } else if (value.length > 150) {
                error = 'Límite de caracteres excedido (150)';
            } else if (/[^a-zA-Z0-9\s,#]/.test(value)) {
                error = 'No se permiten caracteres especiales (ª!"$%&/()=?)';
            } else if (/\s{2,}/.test(value)) {
                error = 'No se permiten más de 2 espacios seguidos';
            }
            break;
        case 'numeroCelular':
            if (!value) {
                error = 'Campo obligatorio';
            } else if (!/^\d{8}$/.test(value)) {
                error = 'El número de celular debe tener 8 dígitos';
            }
            break;
        case 'correoElectronico':
            if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                error = 'Correo electrónico inválido';
            }
            break;
    }

    errorElement.textContent = error;
    return error === '';
}

function validateSection(sectionNumber) {
    const section = document.getElementById(`section${sectionNumber}`);
    const fields = section.querySelectorAll('input, select');
    let isValid = true;

    fields.forEach(field => {
        if (field.required && !validateField(field)) {
            isValid = false;
        }
    });

    return isValid;
}

function updateNextButtonState() {
    nextBtn.disabled = !validateSection(currentSection);
}

nextBtn.addEventListener('click', () => {
    if (validateSection(currentSection)) {
        currentSection++;
        showSection(currentSection);
        updateNextButtonState();
    }
});

prevBtn.addEventListener('click', () => {
    currentSection--;
    showSection(currentSection);
    updateNextButtonState();
});

form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (validateSection(currentSection)) {
        alert('Formulario enviado con éxito!');
        // Aquí puedes agregar la lógica para enviar el formulario
    }
});

// Inicializar
updateProgressBar();

// Validación en tiempo real
form.querySelectorAll('input, select').forEach(field => {
    field.addEventListener('input', () => {
        validateField(field);
        updateNextButtonState();
    });
});

// Lógica para habilitar/deshabilitar selects de Provincia y Municipio
const departamentoSelect = document.getElementById('departamento');
const provinciaSelect = document.getElementById('provincia');
const municipioSelect = document.getElementById('municipio');

departamentoSelect.addEventListener('change', () => {
    const selectedDepartamento = departamentoSelect.value;
    provinciaSelect.disabled = !selectedDepartamento;
    municipioSelect.disabled = true;
    provinciaSelect.innerHTML = '<option value="">Seleccione su Provincia</option>';
    municipioSelect.innerHTML = '<option value="">Seleccione su Municipio</option>';
    
    if (selectedDepartamento && provincias[selectedDepartamento]) {
        provincias[selectedDepartamento].forEach(provincia => {
            const option = document.createElement('option');
            option.value = provincia;
            option.textContent = provincia;
            provinciaSelect.appendChild(option);
        });
    }
});

provinciaSelect.addEventListener('change', () => {
    const selectedDepartamento = departamentoSelect.value;
    const selectedProvincia = provinciaSelect.value;
    municipioSelect.disabled = !selectedProvincia;
    municipioSelect.innerHTML = '<option value="">Seleccione su Municipio</option>';
    
    if (selectedDepartamento && municipios[selectedDepartamento]) {
        municipios[selectedDepartamento].forEach(municipio => {
            const option = document.createElement('option');
            option.value = municipio;
            option.textContent = municipio;
            municipioSelect.appendChild(option);
        });
    }
});

// Autocompletar "@" en el nombre de usuario
const nombreUsuarioInput = document.getElementById('nombreUsuario');
nombreUsuarioInput.addEventListener('input', function(e) {
    if (!this.value.startsWith('@') && this.value.length > 0) {
        this.value = '@' + this.value;
    }
});

function handleImagePreview(inputElement, previewElement, chooseFileText, fileFormatText, imageIcon, fileButton) {
inputElement.addEventListener('change', function(e) {
const file = e.target.files[0];
if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Limpiar cualquier vista previa anterior
        previewElement.innerHTML = ''; 

        // Crear la imagen y agregarla al contenedor de vista previa
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.width = '100%';  // Ajusta el tamaño de la imagen
        img.style.height = 'auto'; // Mantener proporción

        // Crear el botón de eliminación
        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'X';
        removeBtn.className = 'remove-image-button'; 

        // Limpiar la imagen cuando se presione la X roja
        removeBtn.addEventListener('click', () => {
            previewElement.innerHTML = ''; 
            inputElement.value = '';  // Restablecer input de archivo
            previewElement.style.display = 'none'; // Ocultar la vista previa

           
            chooseFileText.style.display = 'block';
            fileFormatText.style.display = 'block';
            imageIcon.style.display = 'block';
            fileButton.style.display = 'block';
        });

        // Agregar la imagen y el botón al contenedor de vista previa
        previewElement.appendChild(img);
        previewElement.appendChild(removeBtn);
        previewElement.style.display = 'block'; // Mostrar la vista previa

        // Ocultar los textos de instrucciones, el ícono y el botón de búsqueda
        chooseFileText.style.display = 'none';
        fileFormatText.style.display = 'none';
        imageIcon.style.display = 'none';
        fileButton.style.display = 'none';
    };
    reader.readAsDataURL(file);
}
});
}

// Previsualización de la foto de perfil
const fotoPerfilInput = document.getElementById('fotoPerfil');
const fotoPerfilPreview = document.getElementById('fotoPerfilPreview');
const chooseFileText1 = document.getElementById('chooseFileText1');
const fileFormatText1 = document.getElementById('fileFormatText1');
const imageIcon1 = document.getElementById('imageIcon1');
const fileButton1 = document.getElementById('fileButton1');
handleImagePreview(fotoPerfilInput, fotoPerfilPreview, chooseFileText1, fileFormatText1, imageIcon1, fileButton1);

// Previsualización del código QR
const codigoQRInput = document.getElementById('codigoQR');
const codigoQRPreview = document.getElementById('codigoQRPreview');
const chooseFileText2 = document.getElementById('chooseFileText2');
const fileFormatText2 = document.getElementById('fileFormatText2');
const imageIcon2 = document.getElementById('imageIcon2');
const fileButton2 = document.getElementById('fileButton2');
handleImagePreview(codigoQRInput, codigoQRPreview, chooseFileText2, fileFormatText2, imageIcon2, fileButton2);

