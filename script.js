async function searchFlag() {
    const countryInput = document.getElementById('countryInput').value.trim();
    const flagDisplay = document.getElementById('flagDisplay');
    const countryFact = document.getElementById('countryFact');

    if (!countryInput) {
        flagDisplay.innerHTML = '<p>Please enter a country name.</p>';
        countryFact.innerHTML = '';
        return;
    }

    flagDisplay.innerHTML = '<p>Searching...</p>';
    countryFact.innerHTML = '';

    try {
        const response = await fetch(`https://restcountries.com/v3.1/name/${countryInput}`);
        if (!response.ok) {
            throw new Error('Country not found');
        }
        const data = await response.json();
        const country = data[0];
        const flagUrl = country.flags.svg;
        const countryName = country.name.common;
        const region = country.region;
        const population = country.population.toLocaleString();
        const capital = country.capital[0];
        const languages = Object.values(country.languages || {}).join(', ');
        const currencies = Object.values(country.currencies || {}).map(curr => curr.name).join(', ');
        const timezones = country.timezones.join(', ');

        flagDisplay.innerHTML = `
            <h2>${countryName}</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start;">
                <div>
                    <img src="${flagUrl}" alt="Flag of ${countryName}" style="width: 100%; max-width: 400px;">
                    <p><strong>Region:</strong> ${region}</p>
                    <p><strong>Population:</strong> ${population}</p>
                </div>
                <div style="font-size: 1.2rem;">
                    <h3 style="font-size: 1.8rem;">Fun Facts about ${countryName}:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 10px;">🏛️ The capital city is ${capital}</li>
                        <li style="margin-bottom: 10px;">🗣️ Official language(s): ${languages}</li>
                        <li style="margin-bottom: 10px;">💰 Currency: ${currencies}</li>
                        <li style="margin-bottom: 10px;">🕒 Timezone(s): ${timezones}</li>
                        ${country.borders ? `<li style="margin-bottom: 10px;">🗺️ Shares borders with ${country.borders.length} countries</li>` : ''}
                        ${country.independent ? '<li style="margin-bottom: 10px;">🏛️ This is an independent country</li>' : ''}
                        ${country.unMember ? '<li style="margin-bottom: 10px;">🌐 Member of the United Nations</li>' : ''}
                    </ul>
                </div>
            </div>
        `;
        countryFact.innerHTML = '';
    } catch (error) {
        flagDisplay.innerHTML = '<p>Country not found. Please try again.</p>';
        countryFact.innerHTML = '';
    }
}

// Add this event listener to handle the Enter key press
document.getElementById('countryInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission if inside a form
        searchFlag();
    }
});
