/**
 * ================================================================
 * VANGUARD LABS – MAIN JAVASCRIPT
 * ================================================================
 * Core initialisation, loader, sticky nav, scroll progress,
 * back-to-top, mobile menu, and general DOM helpers.
 * ================================================================
 */

(function () {
    'use strict';

    // ---- DOM refs ----
    const loader = document.getElementById('loader');
    const header = document.getElementById('main-header');
    const progressBar = document.getElementById('scroll-progress');
    const backBtn = document.getElementById('back-to-top');
    const mobileToggle = document.getElementById('mobile-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    // ---- 1. LOADER ----
    if (loader) {
        window.addEventListener('load', function () {
            setTimeout(function () {
                loader.classList.add('hidden');
            }, 600);
        });
        // Fallback: hide after 3s if window.load doesn't fire
        setTimeout(function () {
            if (!loader.classList.contains('hidden')) {
                loader.classList.add('hidden');
            }
        }, 3500);
    }

    // ---- 2. STICKY HEADER ----
    if (header) {
        let lastScroll = 0;
        window.addEventListener('scroll', function () {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 80) {
                header.classList.add('bg-black/80', 'backdrop-blur-xl', 'border-b', 'border-white/5');
            } else {
                header.classList.remove('bg-black/80', 'backdrop-blur-xl', 'border-b', 'border-white/5');
            }
            lastScroll = currentScroll;
        });
    }

    // ---- 3. SCROLL PROGRESS ----
    if (progressBar) {
        window.addEventListener('scroll', function () {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = progress + '%';
        });
    }

    // ---- 4. BACK-TO-TOP ----
    if (backBtn) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                backBtn.classList.add('visible');
            } else {
                backBtn.classList.remove('visible');
            }
        });
        backBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ---- 5. MOBILE MENU ----
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function () {
            const isHidden = mobileMenu.classList.contains('hidden');
            mobileMenu.classList.toggle('hidden');
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
    }

    // ---- 6. SMOOTH SCROLL FOR ANCHOR LINKS ----
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // ---- 7. FADE-IN ON SCROLL (Intersection Observer) ----
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
    if (fadeElements.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -20px 0px' });
        fadeElements.forEach(function (el) {
            observer.observe(el);
        });
    }
})();
