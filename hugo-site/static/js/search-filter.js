// Advanced Car Search and Filter System

class CarSearchFilter {
    constructor() {
        this.cars = [];
        this.filteredCars = [];
        this.currentFilters = {};
        this.init();
    }

    init() {
        this.loadCarsData();
        this.bindEvents();
        this.parseUrlParams();
    }

        // Load cars data from the page
    loadCarsData() {
        const carCards = document.querySelectorAll('.car-card');
        this.cars = Array.from(carCards).map(card => {
            const titleEl = card.querySelector('.card-title a');

            // Get data from data attributes (preferred method)
            const brand = card.dataset.brand || '';
            const model = card.dataset.model || '';
            const year = parseInt(card.dataset.year) || 0;
            const price = parseInt(card.dataset.price) || 0;
            const mileage = parseInt(card.dataset.mileage) || 0;
            const engine = card.dataset.engine || '';
            const transmission = card.dataset.transmission || '';
            const bodyType = card.dataset.body || '';
            const fuelType = card.dataset.fuel || '';
            const condition = card.dataset.condition || '';

            // Fallback: extract from text content if data attributes are missing
            const titleText = titleEl ? titleEl.textContent.trim() : '';
            const brandText = card.querySelector('.text-muted')?.textContent?.trim() || '';
            const priceEl = card.querySelector('.badge.bg-primary, .text-primary, .price-amount');
            const priceText = priceEl ? priceEl.textContent.trim() : '';

            // Parse fallback data if needed
            const fallbackPrice = price || parseInt(priceText.replace(/[^\d]/g, '')) || 0;
            const fallbackBrand = brand || (brandText.includes('•') ? brandText.split('•')[0].trim().split(' ')[0] : titleText.split(' ')[0]) || '';
            const fallbackModel = model || (brandText.includes('•') ? brandText.split('•')[0].trim().split(' ')[1] : titleText.split(' ')[1]) || '';
            const fallbackYear = year || parseInt((brandText.includes('•') ? brandText.split('•')[1] : titleText.split(' ')[2] || '').replace(/[^\d]/g, '')) || 0;

            const carData = {
                element: card,
                title: titleText,
                brand: fallbackBrand,
                model: fallbackModel,
                year: fallbackYear,
                price: fallbackPrice,
                mileage: mileage,
                engine: engine,
                transmission: transmission,
                bodyType: bodyType,
                fuelType: fuelType,
                condition: condition,
                url: titleEl ? titleEl.href : ''
            };

            console.log('Car data:', carData); // Debug log
            return carData;
        });

        this.filteredCars = [...this.cars];
        console.log('Loaded cars:', this.cars.length);
        console.log('Cars with prices:', this.cars.filter(car => car.price > 0).length);
    }

    extractBodyType(card) {
        const features = card.querySelectorAll('.car-features-list li, .feature-item');
        for (let feature of features) {
            const text = feature.textContent.toLowerCase();
            if (text.includes('седан')) return 'Седан';
            if (text.includes('внедорожник')) return 'Внедорожник';
            if (text.includes('хэтчбек')) return 'Хэтчбек';
            if (text.includes('универсал')) return 'Универсал';
            if (text.includes('купе')) return 'Купе';
        }
        return '';
    }

    extractFuelType(card) {
        const features = card.querySelectorAll('.car-features-list li, .feature-item');
        for (let feature of features) {
            const text = feature.textContent.toLowerCase();
            if (text.includes('бензин')) return 'Бензин';
            if (text.includes('дизель')) return 'Дизель';
            if (text.includes('гибрид')) return 'Гибрид';
            if (text.includes('электро')) return 'Электро';
        }
        return 'Бензин'; // Default
    }

    bindEvents() {
        // Form submission
        const forms = document.querySelectorAll('.car-search-form, .filters-form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.applyFilters();
            });
        });

        // Real-time filtering
        const filterInputs = document.querySelectorAll(
            '#brand, #model, #price_from, #price_to, #year_from, #year_to, #body_type, #fuel_type, #transmission'
        );

        filterInputs.forEach(input => {
            input.addEventListener('change', () => {
                this.applyFilters();
            });
        });

        // Search input with debounce
        const searchInput = document.querySelector('#search, input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(() => {
                this.applyFilters();
            }, 300));
        }

        // Reset filters
        const resetButtons = document.querySelectorAll('[href*="cars/"], .btn-reset');
        resetButtons.forEach(btn => {
            if (btn.textContent.includes('Сбросить') || btn.textContent.includes('Reset')) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.resetFilters();
                });
            }
        });
    }

    parseUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);

        this.currentFilters = {
            brand: urlParams.get('brand') || '',
            model: urlParams.get('model') || '',
            price_from: parseInt(urlParams.get('price_from')) || 0,
            price_to: parseInt(urlParams.get('price_to')) || 0,
            year_from: parseInt(urlParams.get('year_from')) || 0,
            year_to: parseInt(urlParams.get('year_to')) || 0,
            body_type: urlParams.get('body_type') || '',
            fuel_type: urlParams.get('fuel_type') || '',
            transmission: urlParams.get('transmission') || '',
            search: urlParams.get('q') || urlParams.get('search') || ''
        };

        // Set form values from URL
        Object.keys(this.currentFilters).forEach(key => {
            const input = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
            if (input && this.currentFilters[key]) {
                input.value = this.currentFilters[key];
            }
        });

        // Apply initial filters
        if (Object.values(this.currentFilters).some(val => val !== '' && val !== 0)) {
            setTimeout(() => this.applyFilters(), 100);
        }
    }

    applyFilters() {
        // Get current filter values
        this.currentFilters = {
            brand: this.getInputValue('#brand'),
            model: this.getInputValue('#model'),
            price_from: parseInt(this.getInputValue('#price_from')) || 0,
            price_to: parseInt(this.getInputValue('#price_to')) || 0,
            year_from: parseInt(this.getInputValue('#year_from')) || 0,
            year_to: parseInt(this.getInputValue('#year_to')) || 0,
            body_type: this.getInputValue('#body_type'),
            fuel_type: this.getInputValue('#fuel_type'),
            transmission: this.getInputValue('#transmission'),
            search: this.getInputValue('#search, input[name="q"]')
        };

                console.log('Applying filters:', this.currentFilters);

        // Filter cars
        this.filteredCars = this.cars.filter(car => {
            // Brand filter
            if (this.currentFilters.brand &&
                !car.brand.toLowerCase().includes(this.currentFilters.brand.toLowerCase())) {
                console.log(`Filtered out ${car.title} by brand: ${car.brand} vs ${this.currentFilters.brand}`);
                return false;
            }

            // Model filter
            if (this.currentFilters.model &&
                !car.model.toLowerCase().includes(this.currentFilters.model.toLowerCase())) {
                console.log(`Filtered out ${car.title} by model: ${car.model} vs ${this.currentFilters.model}`);
                return false;
            }

            // Price filters
            if (this.currentFilters.price_from > 0 && car.price < this.currentFilters.price_from) {
                console.log(`Filtered out ${car.title} by price_from: ${car.price} < ${this.currentFilters.price_from}`);
                return false;
            }
            if (this.currentFilters.price_to > 0 && car.price > this.currentFilters.price_to) {
                console.log(`Filtered out ${car.title} by price_to: ${car.price} > ${this.currentFilters.price_to}`);
                return false;
            }

            // Year filters
            if (this.currentFilters.year_from > 0 && car.year < this.currentFilters.year_from) {
                console.log(`Filtered out ${car.title} by year_from: ${car.year} < ${this.currentFilters.year_from}`);
                return false;
            }
            if (this.currentFilters.year_to > 0 && car.year > this.currentFilters.year_to) {
                console.log(`Filtered out ${car.title} by year_to: ${car.year} > ${this.currentFilters.year_to}`);
                return false;
            }

            // Body type filter
            if (this.currentFilters.body_type &&
                !car.bodyType.toLowerCase().includes(this.currentFilters.body_type.toLowerCase())) {
                console.log(`Filtered out ${car.title} by body_type: ${car.bodyType} vs ${this.currentFilters.body_type}`);
                return false;
            }

            // Fuel type filter
            if (this.currentFilters.fuel_type &&
                !car.fuelType.toLowerCase().includes(this.currentFilters.fuel_type.toLowerCase())) {
                console.log(`Filtered out ${car.title} by fuel_type: ${car.fuelType} vs ${this.currentFilters.fuel_type}`);
                return false;
            }

            // Transmission filter
            if (this.currentFilters.transmission &&
                !car.transmission.toLowerCase().includes(this.currentFilters.transmission.toLowerCase())) {
                console.log(`Filtered out ${car.title} by transmission: ${car.transmission} vs ${this.currentFilters.transmission}`);
                return false;
            }

            // Search filter (title, brand, model)
            if (this.currentFilters.search) {
                const searchText = this.currentFilters.search.toLowerCase();
                const searchableText = `${car.title} ${car.brand} ${car.model}`.toLowerCase();
                if (!searchableText.includes(searchText)) {
                    console.log(`Filtered out ${car.title} by search: ${searchableText} vs ${searchText}`);
                    return false;
                }
            }

            console.log(`Passed all filters: ${car.title}`);
            return true;
        });

        console.log(`Filter results: ${this.filteredCars.length} of ${this.cars.length} cars`);

        this.renderResults();
        this.updateUrl();
        this.updateResultsCount();
    }

    renderResults() {
        // Hide all cars
        this.cars.forEach(car => {
            car.element.style.display = 'none';
            car.element.parentElement.style.display = 'none';
        });

        // Show filtered cars
        this.filteredCars.forEach(car => {
            car.element.style.display = 'block';
            car.element.parentElement.style.display = 'block';
        });

        // Show/hide no results message
        this.toggleNoResultsMessage();

        // Add animation
        this.filteredCars.forEach((car, index) => {
            setTimeout(() => {
                car.element.classList.add('fade-in-up');
            }, index * 50);
        });
    }

    toggleNoResultsMessage() {
        let noResultsEl = document.querySelector('.no-results-message');
        const container = document.querySelector('#cars-container, .cars-grid .row');

        if (this.filteredCars.length === 0) {
            if (!noResultsEl && container) {
                noResultsEl = document.createElement('div');
                noResultsEl.className = 'col-12 text-center py-5 no-results-message';
                noResultsEl.innerHTML = `
                    <div class="no-results">
                        <i class="fas fa-search fa-3x text-muted mb-3"></i>
                        <h4>Автомобили не найдены</h4>
                        <p class="text-muted">Попробуйте изменить параметры поиска</p>
                        <button class="btn btn-primary" onclick="carFilter.resetFilters()">
                            Сбросить фильтры
                        </button>
                    </div>
                `;
                container.appendChild(noResultsEl);
            }
            if (noResultsEl) noResultsEl.style.display = 'block';
        } else {
            if (noResultsEl) noResultsEl.style.display = 'none';
        }
    }

    updateResultsCount() {
        const countElements = document.querySelectorAll('.results-count, .cars-count');
        countElements.forEach(el => {
            el.textContent = `Показано ${this.filteredCars.length} из ${this.cars.length} автомобилей`;
        });

        // Update page title
        const titleEl = document.querySelector('h1, .page-title');
        if (titleEl && this.filteredCars.length !== this.cars.length) {
            const originalTitle = titleEl.dataset.originalTitle || titleEl.textContent;
            titleEl.dataset.originalTitle = originalTitle;
            titleEl.textContent = `${originalTitle} (${this.filteredCars.length})`;
        }
    }

    updateUrl() {
        const params = new URLSearchParams();

        Object.keys(this.currentFilters).forEach(key => {
            if (this.currentFilters[key] && this.currentFilters[key] !== '' && this.currentFilters[key] !== 0) {
                params.set(key, this.currentFilters[key]);
            }
        });

        const newUrl = params.toString() ?
            `${window.location.pathname}?${params.toString()}` :
            window.location.pathname;

        window.history.replaceState({}, '', newUrl);
    }

    resetFilters() {
        // Clear form inputs
        const inputs = document.querySelectorAll(
            '#brand, #model, #price_from, #price_to, #year_from, #year_to, #body_type, #fuel_type, #transmission, #search, input[name="q"]'
        );
        inputs.forEach(input => {
            input.value = '';
            if (input.type === 'select-one') {
                input.selectedIndex = 0;
            }
        });

        // Don't manage model dropdown here - it's handled by index.html script
        // The brand/model selector logic is now in index.html

        // Clear filters and show all cars
        this.currentFilters = {};
        this.filteredCars = [...this.cars];
        this.renderResults();
        this.updateUrl();
        this.updateResultsCount();

        // Update floating labels
        if (window.updateFloatingLabels) {
            window.updateFloatingLabels();
        }
    }

    getInputValue(selector) {
        const input = document.querySelector(selector);
        return input ? input.value.trim() : '';
    }

    debounce(func, wait) {
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

    // Public methods for external access
    filterByBrand(brand) {
        const brandSelect = document.getElementById('brand');
        if (brandSelect) {
            brandSelect.value = brand;
            this.applyFilters();
        }
    }

    filterByPrice(min, max) {
        const priceFromInput = document.getElementById('price_from');
        const priceToInput = document.getElementById('price_to');

        if (priceFromInput) priceFromInput.value = min || '';
        if (priceToInput) priceToInput.value = max || '';

        this.applyFilters();
    }
}

// Initialize filter system when DOM is loaded
let carFilter;

document.addEventListener('DOMContentLoaded', function() {
    // Only initialize on cars pages
    if (window.location.pathname.includes('/cars') || document.querySelector('.car-card')) {
        carFilter = new CarSearchFilter();

        // Make it globally accessible
        window.carFilter = carFilter;

        console.log('Car Search Filter initialized');
    }
});
