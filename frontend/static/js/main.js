// main.js - General functionality for the site

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    
    const nav = document.querySelector('.nav');
    const header = document.querySelector('.header .container');
    
    if (window.innerWidth < 768) {
        header.appendChild(mobileMenuToggle);
        nav.classList.add('hidden');
    }
    
    mobileMenuToggle.addEventListener('click', function() {
        nav.classList.toggle('hidden');
        this.innerHTML = nav.classList.contains('hidden') 
            ? '<i class="fas fa-bars"></i>' 
            : '<i class="fas fa-times"></i>';
    });
    
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            nav.classList.remove('hidden');
            if (header.contains(mobileMenuToggle)) {
                header.removeChild(mobileMenuToggle);
            }
        } else {
            if (!header.contains(mobileMenuToggle)) {
                header.appendChild(mobileMenuToggle);
            }
            nav.classList.add('hidden');
        }
    });
    
    // Add active class to current page in navigation
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav a');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage || 
            (currentPage === '' && linkPage === 'index.html')) {
            link.classList.add('active');
        }
    });
});
