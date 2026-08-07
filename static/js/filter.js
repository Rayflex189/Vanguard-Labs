/**
 * ================================================================
 * VANGUARD LABS – FILTER (client‑side)
 * ================================================================
 * Filters items (projects, services, etc.) by category using
 * data attributes. Supports search input as well.
 * ================================================================
 */

(function () {
    'use strict';

    // ---- Config ----
    const FILTER_CONTAINER = document.querySelector('[data-filter-container]');
    const FILTER_ITEMS = FILTER_CONTAINER ? FILTER_CONTAINER.querySelectorAll('[data-filter-item]') : [];
    const FILTER_BUTTONS = document.querySelectorAll('[data-filter-btn]');
    const SEARCH_INPUT = document.querySelector('[data-filter-search]');

    if (!FILTER_CONTAINER || FILTER_ITEMS.length === 0) return;

    // ---- Helper to show/hide ----
    function filterItems(category, searchTerm) {
        const search = searchTerm ? searchTerm.toLowerCase().trim() : '';
        FILTER_ITEMS.forEach(function (item) {
            const categories = (item.dataset.filterCategory || '').split(',').map(function (c) { return c.trim(); });
            const title = (item.dataset.filterTitle || item.textContent || '').toLowerCase();
            let matchCategory = true;
            if (category && category !== 'all') {
                matchCategory = categories.indexOf(category) !== -1;
            }
            let matchSearch = true;
            if (search) {
                matchSearch = title.indexOf(search) !== -1;
            }
            item.style.display = (matchCategory && matchSearch) ? '' : 'none';
        });
    }

    // ---- Button click ----
    FILTER_BUTTONS.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const category = this.dataset.filterBtn;
            // Update active button
            FILTER_BUTTONS.forEach(function (b) { b.classList.remove('active'); });
            this.classList.add('active');
            const search = SEARCH_INPUT ? SEARCH_INPUT.value : '';
            filterItems(category, search);
        });
    });

    // ---- Search input ----
    if (SEARCH_INPUT) {
        SEARCH_INPUT.addEventListener('input', function () {
            const activeBtn = document.querySelector('[data-filter-btn].active');
            const category = activeBtn ? activeBtn.dataset.filterBtn : 'all';
            filterItems(category, this.value);
        });
    }

    // ---- Initial filter (show all) ----
    filterItems('all', '');
})();
