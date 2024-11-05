document.addEventListener('DOMContentLoaded', function() {
    // ... (previous code remains unchanged) ...

    // New variables for pagination and grid view
    const productsPerPage = 12;
    let currentPage = 1;
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageNumberSpan = document.getElementById('pageNumber');
    const viewButtons = document.querySelectorAll('.view-button');
    const productsContainer = document.querySelector('.products-container');

    // Function to update pagination buttons
    function updatePaginationButtons() {
        const totalProducts = document.querySelectorAll('.product:not([style*="display: none"])').length;
        const totalPages = Math.ceil(totalProducts / productsPerPage);
        
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
        pageNumberSpan.textContent = currentPage;
    }

    // Function to show products for current page
    function showProductsForPage(page) {
        const products = document.querySelectorAll('.product:not([style*="display: none"])');
        const startIndex = (page - 1) * productsPerPage;
        const endIndex = startIndex + productsPerPage;

        products.forEach((product, index) => {
            if (index >= startIndex && index < endIndex) {
                product.style.display = '';
            } else {
                product.style.display = 'none';
            }
        });

        updatePaginationButtons();
    }

    // Event listeners for pagination buttons
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            showProductsForPage(currentPage);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        const totalProducts = document.querySelectorAll('.product:not([style*="display: none"])').length;
        const totalPages = Math.ceil(totalProducts / productsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            showProductsForPage(currentPage);
        }
    });

    // Event listeners for view buttons
    viewButtons.forEach(button => {
        button.addEventListener('click', () => {
            const view = button.dataset.view;
            productsContainer.className = `products-container ${view}-view`;
            viewButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    // Toggle filter dropdown visibility
    function toggleDropdown(dropdown) {
        dropdown.classList.toggle('active');
        const isActive = dropdown.classList.contains('active');
        const allDropdowns = document.querySelectorAll('.filter-dropdown');

        // Close other dropdowns if one is opened
        allDropdowns.forEach(d => {
            if (d !== dropdown) {
                d.classList.remove('active');
            }
        });
    }

    // Event listeners for filter buttons
    document.querySelectorAll('.filter-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const dropdownId = event.currentTarget.id.replace('Btn', 'Dropdown');
            const dropdown = document.getElementById(dropdownId);
            toggleDropdown(dropdown);
        });
    });

    // Update the applyFilters function to include pagination
    function applyFilters() {
        const products = document.querySelectorAll('.product');
        const selectedCategories = Array.from(document.querySelectorAll('#categoryDropdown input:checked'))
            .map(input => input.value);
        const selectedPrice = document.querySelector('input[name="price"]:checked')?.value;
        const selectedSort = document.querySelector('input[name="sort"]:checked')?.value;

        products.forEach(product => {
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

            productsArray.forEach(product => productsContainer.appendChild(product));
        }

        // Reset to first page and update pagination
        currentPage = 1;
        showProductsForPage(currentPage);
    }

    // ... (previous event listeners remain unchanged) ...

    // Initial setup
    showProductsForPage(currentPage);
});
