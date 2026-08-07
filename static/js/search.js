/**
 * ================================================================
 * VANGUARD LABS – GLOBAL SEARCH
 * ================================================================
 * Fetches suggestions from /search/ endpoint and displays a dropdown.
 * ================================================================
 */

(function () {
    'use strict';

    const searchInput = document.getElementById('global-search-input');
    const searchDropdown = document.getElementById('global-search-dropdown');
    const searchForm = document.getElementById('global-search-form');

    if (!searchInput || !searchDropdown) return;

    let debounceTimer = null;

    // ---- Fetch suggestions ----
    function fetchSuggestions(query) {
        if (!query || query.length < 2) {
            searchDropdown.innerHTML = '';
            searchDropdown.classList.add('hidden');
            return;
        }

        fetch('/search/?q=' + encodeURIComponent(query))
            .then(function (response) {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(function (data) {
                renderSuggestions(data);
            })
            .catch(function (error) {
                console.warn('Search fetch error:', error);
                searchDropdown.innerHTML = '<div class="p-4 text-white/50">Unable to load suggestions</div>';
                searchDropdown.classList.remove('hidden');
            });
    }

    // ---- Render dropdown ----
    function renderSuggestions(results) {
        if (!results || results.length === 0) {
            searchDropdown.innerHTML = '<div class="p-4 text-white/50 text-sm">No results found</div>';
            searchDropdown.classList.remove('hidden');
            return;
        }

        let html = '';
        results.forEach(function (item) {
            html += `
                <a href="${item.url}" class="flex items-center gap-3 px-4 py-3 hover:bg-white/5 transition border-b border-white/5 last:border-0">
                    <span class="text-xs px-2 py-1 rounded bg-blue-500/20 text-blue-300">${item.category || 'Result'}</span>
                    <span class="text-white text-sm">${item.name}</span>
                </a>
            `;
        });
        searchDropdown.innerHTML = html;
        searchDropdown.classList.remove('hidden');
    }

    // ---- Input handler with debounce ----
    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();
        debounceTimer = setTimeout(function () {
            fetchSuggestions(query);
        }, 300);
    });

    // ---- Close dropdown on outside click ----
    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
            searchDropdown.classList.add('hidden');
        }
    });

    // ---- Submit form (redirect to search results page) ----
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = '/search/?q=' + encodeURIComponent(query);
            }
        });
    }
})();
