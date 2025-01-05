async function searchFlag() {
    const countryInput = document.getElementById('countryInput').value.trim();
    const flagDisplay = document.getElementById('flagDisplay');

    if (!countryInput) {
        flagDisplay.innerHTML = '<p>Please enter a country name.</p>';
        return;
    }

    flagDisplay.innerHTML = '<p>Searching...</p>';

    try {
        const response = await fetch(`https://restcountries.com/v3.1/name/${countryInput}`);
        if (!response.ok) {
            throw new Error('Country not found');
        }
        const data = await response.json();
        const flagUrl = data[0].flags.svg;
        const countryName = data[0].name.common;
        const region = data[0].region;
        const population = data[0].population.toLocaleString();

        flagDisplay.innerHTML = `
            <h2>${countryName}</h2>
            <img src="${flagUrl}" alt="Flag of ${countryName}">
            <p><strong>Region:</strong> ${region}</p>
            <p><strong>Population:</strong> ${population}</p>
        `;
    } catch (error) {
        flagDisplay.innerHTML = '<p>Country not found. Please try again.</p>';
    }
}
