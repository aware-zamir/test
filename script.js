/**
 * CountryFlagFinder - A professional implementation for searching and displaying country flags
 * Using the REST Countries API v3.1
 */

class CountryFlagFinder {
    constructor() {
        this.API_BASE_URL = 'https://restcountries.com/v3.1';
        this.initializeEventListeners();
        this.injectStyles();
    }

    initializeEventListeners() {
        const input = document.getElementById('countryInput');
        const searchButton = document.getElementById('searchButton');
        
        if (input) {
            input.addEventListener('keypress', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    this.searchFlag();
                }
            });
        }

        if (searchButton) {
            searchButton.addEventListener('click', () => this.searchFlag());
        }
    }

    async searchFlag() {
        const countryInput = document.getElementById('countryInput')?.value.trim();
        const flagDisplay = document.getElementById('flagDisplay');

        if (!flagDisplay || !countryInput) {
            this.displayError('Please enter a country name.');
            return;
        }

        this.displayLoading();

        try {
            const country = await this.fetchCountryData(countryInput);
            if (country) {
                this.renderCountryCard(country, flagDisplay);
            }
        } catch (error) {
            this.displayError('Country not found. Please try again.');
        }
    }

    async fetchCountryData(countryName) {
        const response = await fetch(`${this.API_BASE_URL}/name/${countryName}`);
        if (!response.ok) throw new Error('Country not found');
        const data = await response.json();
        return data[0];
    }

    renderCountryCard(country, container) {
        const { flags, name, region, population } = country;
        
        container.innerHTML = `
            <div class="country-card">
                <h2 class="country-title">${name.common}</h2>
                <div class="flag-container">
                    <img class="flag-image" src="${flags.svg}" alt="Flag of ${name.common}" loading="lazy">
                    <div class="country-info">
                        <p class="info-item"><strong>Region:</strong> ${region}</p>
                        <p class="info-item"><strong>Population:</strong> ${population.toLocaleString()}</p>
                    </div>
                </div>
            </div>
        `;
    }

    displayError(message) {
        const flagDisplay = document.getElementById('flagDisplay');
        if (flagDisplay) {
            flagDisplay.innerHTML = `<p class="error-message">${message}</p>`;
        }
    }

    displayLoading() {
        const flagDisplay = document.getElementById('flagDisplay');
        if (flagDisplay) {
            flagDisplay.innerHTML = '<p class="loading">Searching...</p>';
        }
    }

    injectStyles() {
        const styles = `
            .country-card { background: #fff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 600px; margin: 20px auto; }
            .country-title { color: #333; font-size: 24px; text-align: center; margin-bottom: 20px; }
            .flag-container { display: flex; flex-direction: column; align-items: center; }
            .flag-image { width: 100%; max-width: 300px; border-radius: 5px; margin: 10px 0; }
            .country-info { text-align: center; margin-top: 15px; }
            .info-item { margin: 5px 0; color: #666; }
            .error-message { color: #e74c3c; text-align: center; padding: 10px; }
            .loading { text-align: center; color: #3498db; padding: 10px; }
            #countryInput { padding: 8px; margin: 10px; border: 1px solid #ddd; border-radius: 4px; }
            #searchButton { padding: 8px 16px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
            #searchButton:hover { background: #2980b9; }
        `;
        const styleElement = document.createElement('style');
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
    }
}

// Initialize the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    new CountryFlagFinder();
});
