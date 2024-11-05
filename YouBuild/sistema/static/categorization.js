document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los elementos necesarios
    const filterButtons = document.querySelectorAll('.filter-button');
    const resetButton = document.getElementById('resetFilters');
    const dropdowns = document.querySelectorAll('.filter-dropdown');
    
    // Función para cerrar todos los dropdowns y remover la clase 'expanded'
    function closeAllDropdowns() {
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
        filterButtons.forEach(button => {
            button.classList.remove('expanded'); // Quita la clase 'expanded' de todos los botones
        });
    }

    // Manejador para los botones de filtro
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const dropdown = this.nextElementSibling;
            
            // Cerrar otros dropdowns
            dropdowns.forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove('active');
                }
            });
            filterButtons.forEach(b => {
                if (b !== this) {
                    b.classList.remove('expanded');
                }
            });
            
            // Alterna el dropdown y la clase 'expanded' en el botón actual
            dropdown.classList.toggle('active');
            button.classList.toggle('expanded');
        });
    });

    // Cerrar dropdowns cuando se hace click fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.filter-group')) {
            closeAllDropdowns();
        }
    });

    // Prevenir que los clicks en el dropdown cierren el menú
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });

    // Función para aplicar filtros
    function applyFilters() {
        const products = document.querySelectorAll('.product');
        const selectedCategories = Array.from(document.querySelectorAll('#categoryDropdown input:checked'))
            .map(input => input.value);
        const selectedPrice = document.querySelector('input[name="price"]:checked')?.value;
        const selectedSort = document.querySelector('input[name="sort"]:checked')?.value;

        products.forEach(product => {
            // Aquí implementarías la lógica de filtrado según tus necesidades
            let shouldShow = true;
            
            // Filtrar por categoría
            if (selectedCategories.length > 0) {
                const productCategory = product.dataset.category;
                shouldShow = selectedCategories.includes(productCategory);
            }

            // Filtrar por precio
            if (shouldShow && selectedPrice) {
                const productPrice = parseFloat(product.dataset.price);
                const [min, max] = selectedPrice.split('-').map(Number);
                shouldShow = productPrice >= min && (!max || productPrice <= max);
            }

            product.style.display = shouldShow ? '' : 'none';
        });

        // Aplicar ordenamiento
        if (selectedSort) {
            const productsArray = Array.from(products);
            productsArray.sort((a, b) => {
                const priceA = parseFloat(a.dataset.price);
                const priceB = parseFloat(b.dataset.price);
                return selectedSort === 'price-asc' ? priceA - priceB : priceB - priceA;
            });

            const container = document.querySelector('.products-container');
            productsArray.forEach(product => container.appendChild(product));
        }
    }

    // Agregar event listeners para los cambios en los filtros
    document.querySelectorAll('.filter-dropdown input').forEach(input => {
        input.addEventListener('change', applyFilters);
    });

    // Restablecer filtros
    resetButton.addEventListener('click', function() {
        document.querySelectorAll('.filter-dropdown input').forEach(input => {
            input.checked = false;
        });
        closeAllDropdowns();
        applyFilters();
    });
});
