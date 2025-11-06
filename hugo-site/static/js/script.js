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
    const baseUrl = document.querySelector('meta[name="baseURL"]')?.content || '';
    fetch(baseUrl + '/cars/models-data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load car models data');
            }
            return response.json();
        })
        .then(data => {
            carModelsData = data;
            console.log('Car models data loaded successfully');
        })
        .catch(error => {
            console.error('Error loading car models:', error);
            // Provide fallback data for development (matches actual catalog)
            carModelsData = {
                brands: {
                    "BMW": { name: "BMW", models: ["3 Series", "X3", "X5"] },
                    "Mercedes-Benz": { name: "Mercedes-Benz", models: ["C-Class", "E200"] },
                    "Toyota": { name: "Toyota", models: ["Camry", "RAV4"] },
                    "Audi": { name: "Audi", models: ["A6"] },
                    "Volkswagen": { name: "Volkswagen", models: ["Tiguan"] },
                    "Hyundai": { name: "Hyundai", models: ["Sonata"] }
                }
            };
        });

    // Brand/Model selection is now handled in index.html
    // This old code has been replaced with new dynamic selector logic
    // Kept only for filter application
    if (brandSelect) {
        brandSelect.addEventListener('change', function() {
            updateFloatingLabels(); // Update floating label state
            // Don't manage modelInput here - it's handled by index.html
            // Apply filters
            filterCars();
        });
    }

    // Model selection handler
    if (modelInput) {
        modelInput.addEventListener('change', function() {
            updateFloatingLabels();
            filterCars();
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

// ===== CAR FILTERING =====
function filterCars() {
    const brandSelect = document.getElementById('brand');
    const modelSelect = document.getElementById('model');
    const priceFromInput = document.getElementById('price_from');
    const priceToInput = document.getElementById('price_to');
    const yearFromInput = document.getElementById('year_from');
    const yearToInput = document.getElementById('year_to');
    const bodyTypeSelect = document.getElementById('body_type');
    const fuelTypeSelect = document.getElementById('fuel_type');
    const transmissionSelect = document.getElementById('transmission');

    // Get filter values
    const selectedBrand = brandSelect ? brandSelect.value : '';
    const selectedModel = modelSelect ? modelSelect.value : '';
    const priceFrom = priceFromInput ? parseInt(priceFromInput.value) || 0 : 0;
    const priceTo = priceToInput ? parseInt(priceToInput.value) || Infinity : Infinity;
    const yearFrom = yearFromInput ? parseInt(yearFromInput.value) || 0 : 0;
    const yearTo = yearToInput ? parseInt(yearToInput.value) || Infinity : Infinity;
    const selectedBodyType = bodyTypeSelect ? bodyTypeSelect.value : '';
    const selectedFuelType = fuelTypeSelect ? fuelTypeSelect.value : '';
    const selectedTransmission = transmissionSelect ? transmissionSelect.value : '';

    // Get all car cards
    const carCards = document.querySelectorAll('.car-card');
    let visibleCount = 0;

    carCards.forEach(card => {
        let show = true;

        // Get car data from the card
        const cardBrand = card.getAttribute('data-brand') || '';
        const cardModel = card.getAttribute('data-model') || '';
        const cardPrice = parseInt(card.getAttribute('data-price')) || 0;
        const cardYear = parseInt(card.getAttribute('data-year')) || 0;
        const cardBodyType = card.getAttribute('data-body') || '';
        const cardFuelType = card.getAttribute('data-fuel') || '';
        const cardTransmission = card.getAttribute('data-transmission') || '';

        // Apply filters
        if (selectedBrand && cardBrand !== selectedBrand) {
            show = false;
        }

        if (selectedModel && cardModel !== selectedModel) {
            show = false;
        }

        if (cardPrice < priceFrom || cardPrice > priceTo) {
            show = false;
        }

        if (cardYear < yearFrom || cardYear > yearTo) {
            show = false;
        }

        if (selectedBodyType && cardBodyType !== selectedBodyType) {
            show = false;
        }

        if (selectedFuelType && cardFuelType !== selectedFuelType) {
            show = false;
        }

        if (selectedTransmission && cardTransmission !== selectedTransmission) {
            show = false;
        }

        // Show/hide card
        const cardContainer = card.closest('.col-lg-4, .col-md-6, .col-12');
        if (cardContainer) {
            if (show) {
                cardContainer.style.display = 'block';
                visibleCount++;
            } else {
                cardContainer.style.display = 'none';
            }
        }
    });

    // Update results count
    const resultsCount = document.querySelector('.results-count');
    if (resultsCount) {
        const totalCount = carCards.length;
        resultsCount.textContent = `Показано ${visibleCount} из ${totalCount} автомобилей`;
    }

    // Show/hide no results message
    const noResultsSection = document.querySelector('.no-results');
    const carsContainer = document.getElementById('cars-container');

    if (visibleCount === 0) {
        if (carsContainer) carsContainer.style.display = 'none';
        if (noResultsSection) {
            noResultsSection.style.display = 'block';
        } else {
            // Create no results message if it doesn't exist
            const container = carsContainer ? carsContainer.parentElement : null;
            if (container) {
                const noResults = document.createElement('div');
                noResults.className = 'no-results text-center py-5';
                noResults.innerHTML = `
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4>Автомобили не найдены</h4>
                    <p class="text-muted">Попробуйте изменить параметры поиска</p>
                    <button class="btn btn-primary" onclick="clearFilters()">
                        Сбросить фильтры
                    </button>
                `;
                container.appendChild(noResults);
            }
        }
    } else {
        if (carsContainer) carsContainer.style.display = 'block';
        if (noResultsSection) noResultsSection.style.display = 'none';
    }
}

// Clear all filters
function clearFilters() {
    const brandSelect = document.getElementById('brand');
    const modelSelect = document.getElementById('model');
    const priceFromInput = document.getElementById('price_from');
    const priceToInput = document.getElementById('price_to');
    const yearFromInput = document.getElementById('year_from');
    const yearToInput = document.getElementById('year_to');
    const bodyTypeSelect = document.getElementById('body_type');
    const fuelTypeSelect = document.getElementById('fuel_type');
    const transmissionSelect = document.getElementById('transmission');

    if (brandSelect) brandSelect.value = '';
    if (modelSelect) {
        modelSelect.value = '';
        // Don't manage disabled state here - it's handled by index.html
        // Just reset the value
    }
    if (priceFromInput) priceFromInput.value = '';
    if (priceToInput) priceToInput.value = '';
    if (yearFromInput) yearFromInput.value = '';
    if (yearToInput) yearToInput.value = '';
    if (bodyTypeSelect) bodyTypeSelect.value = '';
    if (fuelTypeSelect) fuelTypeSelect.value = '';
    if (transmissionSelect) transmissionSelect.value = '';

    updateFloatingLabels();
    filterCars();
}

// Add event listeners for additional filters
document.addEventListener('DOMContentLoaded', function() {
    // Add listeners for price and year inputs
    const additionalFilters = ['price_from', 'price_to', 'year_from', 'year_to', 'body_type', 'fuel_type', 'transmission'];

    additionalFilters.forEach(filterId => {
        const element = document.getElementById(filterId);
        if (element) {
            element.addEventListener('change', filterCars);
            element.addEventListener('input', debounce(filterCars, 300)); // Debounce for text inputs
        }
    });
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
