// Get current year for the footer
const currentYear = new Date().getFullYear();
const yearSpan = document.getElementById('current-year');
if (yearSpan) {
    yearSpan.textContent = currentYear;
}

// --- Mobile Menu Toggle ---
const menuToggle = document.querySelector('.mobile-menu-toggle');
const mainNav = document.querySelector('.main-nav');

if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
        mainNav.classList.toggle('active'); // Toggles the 'active' class to show/hide
        // Optional: Change button icon (e.g., to 'X')
        if (mainNav.classList.contains('active')) {
            menuToggle.innerHTML = '×'; // Change to 'X'
            menuToggle.setAttribute('aria-expanded', 'true');
        } else {
            menuToggle.innerHTML = '☰'; // Change back to hamburger
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    });
}

// --- Optional: Close Mobile Menu When a Link is Clicked ---
const navLinks = document.querySelectorAll('.main-nav a');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (mainNav.classList.contains('active')) {
             mainNav.classList.remove('active');
             menuToggle.innerHTML = '☰'; // Reset hamburger icon
             menuToggle.setAttribute('aria-expanded', 'false');
        }
    });
});


// --- Optional: Header transparency change on scroll ---
// const header = document.querySelector('.main-header');
// const scrollThreshold = 50; // Pixels to scroll before changing header

// window.addEventListener('scroll', () => {
//   if (window.scrollY > scrollThreshold) {
//     header.classList.add('scrolled');
//   } else {
//     header.classList.remove('scrolled');
//   }
// });