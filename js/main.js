// Signal that JS is active so scroll-reveal hidden states apply (see styles.css .js .reveal).
// Without this class, content is visible by default (no-JS / crawler safe).
document.documentElement.classList.add('js');

// Navbar Scroll Effect
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Scroll Reveal Animations using Intersection Observer
const revealElements = document.querySelectorAll('.reveal, .reveal-delay');

const revealOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
};

const revealOnScroll = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return;
        } else {
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        }
    });
}, revealOptions);

revealElements.forEach(el => {
    revealOnScroll.observe(el);
});

// Trigger initial reveal for elements already in viewport
window.addEventListener('load', () => {
    revealElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if(rect.top < window.innerHeight) {
            el.classList.add('active');
        }
    });
});

// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinksContainer = document.querySelector('.nav-links-container');

if (mobileMenuToggle && navLinksContainer) {
    mobileMenuToggle.addEventListener('click', () => {
        const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
        mobileMenuToggle.setAttribute('aria-expanded', !isExpanded);
        navLinksContainer.classList.toggle('active');
    });
}

// Set active navigation link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    // Normalize paths to ignore .html and trailing slashes
    const normalizePath = (p) => p.replace(/\/$/, '').replace(/\.html$/, '') || '/';
    const normalizedCurrentPath = normalizePath(currentPath);

    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        const normalizedLinkPath = normalizePath(linkPath);
        
        if (normalizedCurrentPath === normalizedLinkPath && normalizedCurrentPath !== '/') {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
});
