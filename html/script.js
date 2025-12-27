/**
 * eGovernment OS Landing Page - Interactive Elements
 * Smooth scrolling, animations, and micro-interactions
 */

// ==================== HAMBURGER MENU ====================
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
});

// Close menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
    });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
    }
});

// ==================== ANIMATED STATISTICS COUNTER ====================
function animateCounter(element, target) {
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60 FPS
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            // Handle percentage values
            if (element.textContent.includes('%')) {
                element.textContent = Math.floor(current) + '%';
            } else {
                element.textContent = Math.floor(current);
            }
            requestAnimationFrame(updateCounter);
        } else {
            // Final value
            if (element.textContent.includes('%')) {
                element.textContent = target + '%';
            } else {
                element.textContent = target;
            }
        }
    };

    updateCounter();
}

// Observe statistics and trigger counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            entry.target.classList.add('counted');
            const statValue = entry.target.querySelector('.stat-value');
            if (statValue) {
                const finalValue = parseInt(statValue.textContent);
                const hasPercent = statValue.textContent.includes('%');
                statValue.textContent = '0' + (hasPercent ? '%' : '');
                animateCounter(statValue, finalValue);
                entry.target.style.animation = 'countUp 0.6s ease forwards';
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat').forEach(stat => {
    statsObserver.observe(stat);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply fade-in to sections
document.querySelectorAll('.feature-card, .glass-card, .experience-text, .security-text').forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(el);
});

// Parallax effect for hero background
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
});

// Add ripple effect to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function (e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation styles
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Email validation for CTA form
const emailInput = document.querySelector('.email-input');
const ctaButton = document.querySelector('.cta-section .btn-primary');

if (ctaButton) {
    ctaButton.addEventListener('click', (e) => {
        e.preventDefault();
        const email = emailInput.value.trim();

        if (!email) {
            showNotification('Please enter your email address', 'warning');
            return;
        }

        if (!isValidEmail(email)) {
            showNotification('Please enter a valid email address', 'warning');
            return;
        }

        showNotification('Thank you! We\'ll be in touch soon.', 'success');
        emailInput.value = '';
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 40px;
        padding: 20px 32px;
        background: ${type === 'success' ? 'rgba(40, 200, 64, 0.95)' : 'rgba(255, 189, 46, 0.95)'};
        color: white;
        border-radius: 12px;
        font-weight: 600;
        font-size: 15px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyle);

// Add mouse move parallax effect for floating cards
document.addEventListener('mousemove', (e) => {
    const cards = document.querySelectorAll('.hero-visual .glass-card');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;

    cards.forEach((card, index) => {
        const speed = (index + 1) * 15;
        const x = (mouseX - 0.5) * speed;
        const y = (mouseY - 0.5) * speed;
        card.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// Navigation background opacity on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.glass-nav');
    if (window.scrollY > 100) {
        nav.style.background = 'rgba(255, 255, 255, 0.1)';
    } else {
        nav.style.background = 'rgba(255, 255, 255, 0.05)';
    }
});

// Add hover tilt effect to feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
});

// ==================== TESTIMONIAL CAROUSEL ====================
const testimonialTrack = document.querySelector('.testimonial-track');
const testimonialCards = document.querySelectorAll('.testimonial-card');
const carouselDots = document.querySelector('.carousel-dots');
const prevBtn = document.querySelector('.carousel-btn.prev');
const nextBtn = document.querySelector('.carousel-btn.next');

let currentTestimonial = 0;
const totalTestimonials = testimonialCards.length;

// Create dots
for (let i = 0; i < totalTestimonials; i++) {
    const dot = document.createElement('div');
    dot.classList.add('carousel-dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToTestimonial(i));
    carouselDots.appendChild(dot);
}

function goToTestimonial(index) {
    currentTestimonial = index;
    const scrollPosition = testimonialCards[index].offsetLeft - (testimonialTrack.offsetWidth - testimonialCards[index].offsetWidth) / 2;
    testimonialTrack.scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
    });
    updateDots();
}

function updateDots() {
    document.querySelectorAll('.carousel-dot').forEach((dot, index) => {
        dot.classList.toggle('active', index === currentTestimonial);
    });
}

function nextTestimonial() {
    currentTestimonial = (currentTestimonial + 1) % totalTestimonials;
    goToTestimonial(currentTestimonial);
}

function prevTestimonial() {
    currentTestimonial = (currentTestimonial - 1 + totalTestimonials) % totalTestimonials;
    goToTestimonial(currentTestimonial);
}

nextBtn.addEventListener('click', nextTestimonial);
prevBtn.addEventListener('click', prevTestimonial);

// Auto-play carousel
let carouselInterval = setInterval(nextTestimonial, 5000);

// Pause on hover
testimonialTrack.addEventListener('mouseenter', () => {
    clearInterval(carouselInterval);
});

testimonialTrack.addEventListener('mouseleave', () => {
    carouselInterval = setInterval(nextTestimonial, 5000);
});

// ==================== ADVANCED SCROLL ANIMATIONS ====================
// Scale and rotate animations
const advancedObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;

            // Add scale effect
            if (element.classList.contains('testimonial-card')) {
                element.style.animation = 'scaleIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards';
            }

            // Add slide from side effects
            if (element.classList.contains('security-visual')) {
                element.style.animation = 'slideFromLeft 1s cubic-bezier(0.4, 0, 0.2, 1) forwards';
            }

            if (element.classList.contains('experience-visual')) {
                element.style.animation = 'slideFromRight 1s cubic-bezier(0.4, 0, 0.2, 1) forwards';
            }
        }
    });
}, { threshold: 0.2 });

// Apply advanced animations
document.querySelectorAll('.testimonial-card, .security-visual, .experience-visual').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'scale(0.9)';
    advancedObserver.observe(el);
});

// Add advanced animation keyframes
const advancedAnimations = document.createElement('style');
advancedAnimations.textContent = `
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9) translateY(30px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    @keyframes slideFromLeft {
        from {
            opacity: 0;
            transform: translateX(-100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideFromRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes rotateIn {
        from {
            opacity: 0;
            transform: rotate(-10deg) scale(0.9);
        }
        to {
            opacity: 1;
            transform: rotate(0) scale(1);
        }
    }
`;
document.head.appendChild(advancedAnimations);

// Parallax scrolling for sections
const parallaxSections = document.querySelectorAll('.features, .testimonials, .cta-section');
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;

    parallaxSections.forEach((section, index) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const scrollPosition = scrolled - sectionTop + window.innerHeight;

        if (scrollPosition > 0 && scrollPosition < sectionHeight + window.innerHeight) {
            const parallaxSpeed = 0.1 * (index + 1);
            const yPos = -(scrollPosition * parallaxSpeed);
            section.style.transform = `translateY(${yPos}px)`;
        }
    });
});

console.log('🚀 eGovernment OS - Ready to transform civic engagement');

