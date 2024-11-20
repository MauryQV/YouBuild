document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    function switchTab(tabId) {
        // Update active state for buttons
        tabButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        // Update active state for content
        tabContents.forEach(content => {
            content.classList.toggle('active', content.id === tabId);
        });

        // Update URL without page reload
        const url = new URL(window.location);
        url.searchParams.set('tab', tabId);
        window.history.pushState({}, '', url);
    }

    // Handle tab clicks
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            switchTab(button.dataset.tab);
        });
    });

    // Handle browser back/forward
    window.addEventListener('popstate', () => {
        const params = new URLSearchParams(window.location.search);
        const activeTab = params.get('tab') || 'todas';
        switchTab(activeTab);
    });

    // Set initial active tab from URL or default to 'todas'
    const params = new URLSearchParams(window.location.search);
    const activeTab = params.get('tab') || 'todas';
    switchTab(activeTab);
});