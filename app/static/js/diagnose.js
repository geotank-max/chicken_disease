document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('symptomSearch');
    const items = document.querySelectorAll('.symptom-item');
    const tabs = document.querySelectorAll('.category-tab');
    let activeCategory = 'all';

    function filterSymptoms() {
        const query = (searchInput?.value || '').toLowerCase().trim();
        items.forEach(item => {
            const cat = item.dataset.category;
            const name = item.dataset.name || '';
            const catMatch = activeCategory === 'all' || cat === activeCategory;
            const searchMatch = !query || name.includes(query) || item.textContent.toLowerCase().includes(query);
            item.style.display = catMatch && searchMatch ? '' : 'none';
        });
    }

    searchInput?.addEventListener('input', filterSymptoms);

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            activeCategory = this.dataset.category;
            filterSymptoms();
        });
    });
});
