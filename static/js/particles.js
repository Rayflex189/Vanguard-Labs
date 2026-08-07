/**
 * ================================================================
 * VANGUARD LABS – PARTICLE BACKGROUND
 * ================================================================
 * Renders animated floating particles with connecting lines.
 * ================================================================
 */

(function () {
    'use strict';

    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    const NUM_PARTICLES = 80;
    const CONNECTION_DIST = 150;
    const PARTICLE_COLOR = '147, 197, 253'; // blue-300

    // ---- Resize handler ----
    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    // ---- Particle class ----
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.4;
            this.speedY = (Math.random() - 0.5) * 0.4;
            this.opacity = Math.random() * 0.5 + 0.2;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            // Bounce off edges
            if (this.x < 0 || this.x > width) this.speedX *= -1;
            if (this.y < 0 || this.y > height) this.speedY *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${PARTICLE_COLOR}, ${this.opacity})`;
            ctx.fill();
        }
    }

    // ---- Initialise particles ----
    for (let i = 0; i < NUM_PARTICLES; i++) {
        particles.push(new Particle());
    }

    // ---- Draw connecting lines ----
    function drawConnections() {
        for (let a = 0; a < particles.length; a++) {
            for (let b = a + 1; b < particles.length; b++) {
                const dx = particles[a].x - particles[b].x;
                const dy = particles[a].y - particles[b].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < CONNECTION_DIST) {
                    const opacity = 0.15 * (1 - dist / CONNECTION_DIST);
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.strokeStyle = `rgba(${PARTICLE_COLOR}, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    // ---- Animation loop ----
    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(function (p) {
            p.update();
            p.draw();
        });
        drawConnections();
        requestAnimationFrame(animate);
    }

    animate();

    // ---- Re-init on resize (optional) ----
    window.addEventListener('resize', function () {
        // Rebuild particles for new dimensions
        particles = [];
        for (let i = 0; i < NUM_PARTICLES; i++) {
            particles.push(new Particle());
        }
    });
})();
