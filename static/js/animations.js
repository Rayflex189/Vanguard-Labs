/**
 * ================================================================
 * VANGUARD LABS – SCROLL ANIMATIONS
 * ================================================================
 * Handles animated counters, progress bars, and any other
 * scroll‑triggered effects.
 * ================================================================
 */

(function () {
    'use strict';

    // ---- 1. ANIMATED COUNTERS ----
    const counters = document.querySelectorAll('.counter');
    if (counters.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.target) || 0;
                    let current = 0;
                    const increment = Math.max(1, Math.ceil(target / 60));
                    const timer = setInterval(function () {
                        current += increment;
                        if (current >= target) {
                            el.textContent = target;
                            clearInterval(timer);
                        } else {
                            el.textContent = current;
                        }
                    }, 20);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.3 });
        counters.forEach(function (c) {
            observer.observe(c);
        });
    }

    // ---- 2. PROGRESS BARS (animated fill) ----
    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const targetWidth = bar.dataset.progress || 0;
                    bar.style.width = targetWidth + '%';
                    observer.unobserve(bar);
                }
            });
        }, { threshold: 0.1 });
        progressBars.forEach(function (bar) {
            observer.observe(bar);
        });
    }

    // ---- 3. TYPING EFFECT (optional) ----
    const typewriter = document.querySelector('.typewriter');
    if (typewriter) {
        const text = typewriter.textContent.trim();
        typewriter.textContent = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                typewriter.textContent += text.charAt(i);
                i++;
                setTimeout(type, 50);
            }
        }
        // Wait for page load and then start
        if (document.readyState === 'complete') {
            type();
        } else {
            window.addEventListener('load', type);
        }
    }
})();
