// Auto Lombard Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {

    // ===== SEARCH FORM ENHANCEMENTS =====
    const searchForm = document.querySelector('.car-search-form');
    const brandSelect = document.getElementById('brand');
    const modelInput = document.getElementById('model');

    // Floating labels for select elements
    function updateFloatingLabels() {
        document.querySelectorAll('.form-floating .form-select').forEach(select => {
            const label = select.nextElementSibling;
            if (select.value && select.value !== "") {
                label.classList.add('active');
                select.classList.add('has-value');
            } else {
                label.classList.remove('active');
                select.classList.remove('has-value');
            }
        });
    }

    // Load car models data
    let carModelsData = {};

    // Fetch car models data
    fetch('/data/car-models.json')
        .then(response => response.json())
        .then(data => {
            carModelsData = data;
        })
        .catch(error => {
            console.error('Error loading car models:', error);
        });

    // Brand selection handler
    if (brandSelect && modelInput) {
        brandSelect.addEventListener('change', function() {
            const selectedBrand = this.value;
            updateFloatingLabels(); // Update floating label state

            if (selectedBrand && carModelsData.brands && carModelsData.brands[selectedBrand]) {
                // Enable model select and populate with models
                modelInput.disabled = false;
                modelInput.innerHTML = '<option value="" selected disabled hidden></option>';

                // Add models for selected brand
                const models = carModelsData.brands[selectedBrand].models;
                models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    modelInput.appendChild(option);
                });

                // Auto-focus model select when brand is selected
                modelInput.focus();
            } else {
                // Disable model select and reset
                modelInput.disabled = true;
                modelInput.innerHTML = '<option value="" selected disabled hidden></option><option value="">Сначала выберите марку</option>';
            }

            updateFloatingLabels(); // Update floating labels after changes
        });
    }

    // Initialize floating labels on page load
    updateFloatingLabels();

    // Handle all select changes
    document.querySelectorAll('.form-floating .form-select').forEach(select => {
        select.addEventListener('change', updateFloatingLabels);
        select.addEventListener('focus', updateFloatingLabels);
        select.addEventListener('blur', updateFloatingLabels);
    });

    // ===== SMOOTH SCROLLING =====
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

    // ===== NAVBAR SCROLL EFFECT =====
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // ===== CAR CARD ANIMATIONS =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe car cards
    document.querySelectorAll('.car-card').forEach(card => {
        observer.observe(card);
    });

    // ===== FORM VALIDATION =====
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add custom validation logic here if needed
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Show error message
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });

    // ===== TELEGRAM WEB APP INTEGRATION =====
    if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;

        // Configure Telegram Web App
        tg.ready();
        tg.expand();

        // Set theme
        document.body.style.backgroundColor = tg.backgroundColor;

        // Add main button if needed
        tg.MainButton.text = "Связаться с нами";
        tg.MainButton.color = "#007bff";
        tg.MainButton.show();

        tg.MainButton.onClick(function() {
            // Handle main button click
            window.location.href = `tel:${document.querySelector('[data-phone]')?.dataset.phone || '+79991234567'}`;
        });

        // Handle back button
        tg.BackButton.onClick(function() {
            if (window.history.length > 1) {
                window.history.back();
            } else {
                tg.close();
            }
        });
    }

    // ===== PHONE NUMBER FORMATTING =====
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value[0] === '8') value = '7' + value.slice(1);
                if (value[0] === '7' && value.length <= 11) {
                    const formatted = value.replace(/(\d)(\d{3})(\d{3})(\d{2})(\d{2})/, '+$1 ($2) $3-$4-$5');
                    e.target.value = formatted;
                }
            }
        });
    });

    // ===== PRICE FORMATTING =====
    const priceElements = document.querySelectorAll('.price-format');
    priceElements.forEach(element => {
        const price = parseInt(element.textContent.replace(/\D/g, ''));
        if (!isNaN(price)) {
            element.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
        }
    });

    // ===== LOADING STATES =====
    const loadingButtons = document.querySelectorAll('.btn-loading');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.disabled = true;
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Загрузка...';

                // Re-enable after 3 seconds (adjust as needed)
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = originalText;
                }, 3000);
            }
        });
    });

    // ===== NOTIFICATION SYSTEM =====
    window.showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    };

    // ===== LAZY LOADING IMAGES =====
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

});

// ===== UTILITY FUNCTIONS =====

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(amount);
}

// Format number with thousands separator
function formatNumber(num) {
    return new Intl.NumberFormat('ru-RU').format(num);
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
