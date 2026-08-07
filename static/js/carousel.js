/**
 * ================================================================
 * VANGUARD LABS – CAROUSEL
 * ================================================================
 * A reusable carousel with arrows, dots, and autoplay.
 * ================================================================
 */

(function () {
    'use strict';

    // ---- Init carousels ----
    document.querySelectorAll('.carousel-container').forEach(function (container) {
        const track = container.querySelector('.carousel-track');
        const items = track ? track.children : [];
        const prevBtn = container.querySelector('.carousel-btn.prev');
        const nextBtn = container.querySelector('.carousel-btn.next');
        const dotsContainer = container.querySelector('.carousel-dots');

        if (!track || items.length === 0) return;

        let currentIndex = 0;
        const totalItems = items.length;
        let autoplayTimer = null;

        // ---- Render dots ----
        if (dotsContainer) {
            dotsContainer.innerHTML = '';
            for (let i = 0; i < totalItems; i++) {
                const dot = document.createElement('button');
                dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
                dot.dataset.index = i;
                dot.addEventListener('click', function () {
                    goTo(parseInt(this.dataset.index));
                });
                dotsContainer.appendChild(dot);
            }
        }

        // ---- Update slide ----
        function goTo(index) {
            if (index < 0) index = totalItems - 1;
            if (index >= totalItems) index = 0;
            currentIndex = index;
            track.style.transform = `translateX(-${currentIndex * 100}%)`;

            // Update dots
            if (dotsContainer) {
                const dots = dotsContainer.querySelectorAll('.carousel-dot');
                dots.forEach(function (dot, i) {
                    dot.classList.toggle('active', i === currentIndex);
                });
            }
        }

        // ---- Navigation ----
        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                goTo(currentIndex - 1);
                resetAutoplay();
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                goTo(currentIndex + 1);
                resetAutoplay();
            });
        }

        // ---- Autoplay ----
        function startAutoplay(interval) {
            stopAutoplay();
            autoplayTimer = setInterval(function () {
                goTo(currentIndex + 1);
            }, interval || 5000);
        }

        function stopAutoplay() {
            if (autoplayTimer) {
                clearInterval(autoplayTimer);
                autoplayTimer = null;
            }
        }

        function resetAutoplay() {
            if (container.dataset.autoplay !== 'false') {
                stopAutoplay();
                startAutoplay(parseInt(container.dataset.interval) || 5000);
            }
        }

        // ---- Start if autoplay enabled ----
        if (container.dataset.autoplay !== 'false') {
            startAutoplay(parseInt(container.dataset.interval) || 5000);
        }

        // ---- Pause on hover ----
        container.addEventListener('mouseenter', function () {
            if (container.dataset.autoplay !== 'false') {
                stopAutoplay();
            }
        });
        container.addEventListener('mouseleave', function () {
            if (container.dataset.autoplay !== 'false') {
                startAutoplay(parseInt(container.dataset.interval) || 5000);
            }
        });

        // ---- Initial setup ----
        goTo(0);
    });
})();
