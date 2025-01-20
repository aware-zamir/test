document.addEventListener('DOMContentLoaded', () => {
    const flagImage = document.getElementById('flag-image');
    const guessInput = document.getElementById('guess-input');
    const submitBtn = document.getElementById('submit-btn');
    const result = document.getElementById('result');
    const nextBtn = document.getElementById('index2.html');

    let currentCountry = '';

    // Function to fetch a random flag
    async function fetchRandomFlag() {
        try {
            const response = await fetch('https://restcountries.com/v3.1/all');
            const countries = await response.json();
            const randomCountry = countries[Math.floor(Math.random() * countries.length)];
            currentCountry = randomCountry.name.common;
            flagImage.src = randomCountry.flags.svg;
            flagImage.alt = `Flag of ${currentCountry}`;
        } catch (error) {
            console.error('Error fetching flag:', error);
            result.textContent = 'Error fetching flag. Please try again later.';
        }
    }

    // Function to check the user's guess
    function checkGuess() {
        const userGuess = guessInput.value.trim().toLowerCase();
        if (userGuess === currentCountry.toLowerCase()) {
            result.textContent = 'Correct! Well done!';
            result.style.color = 'green';
        } else {
            result.textContent = `Wrong! The correct answer was ${currentCountry}.`;
            result.style.color = 'red';
        }
        guessInput.value = '';
        fetchRandomFlag();
    }

    // Event listener for the submit button
    submitBtn.addEventListener('click', checkGuess);

    // Event listener for the "Next" button
    nextBtn.addEventListener('click', () => {
        window.location.href = 'index2.html';
    });

    // Fetch the first random flag when the page loads
    fetchRandomFlag();
});