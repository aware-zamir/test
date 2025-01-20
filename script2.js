document.addEventListener('DOMContentLoaded', () => {
    const languageScript = document.getElementById('language-script');
    const guessInput = document.getElementById('guess-input');
    const submitBtn = document.getElementById('submit-btn');
    const result = document.getElementById('result');
    const nextBtn = document.getElementById('index3.html');
    const backBtn = document.getElementById('index.html');

    let currentLanguage = '';
    let currentCountry = '';

    // Function to fetch a random one-liner in a random language
    const fetchRandomLanguage = async () => {
        try {
            const response = await fetch('https://restcountries.com/v3.1/all');
            const countries = await response.json();
            const randomCountry = countries[Math.floor(Math.random() * countries.length)];
            const languages = randomCountry.languages ? Object.values(randomCountry.languages) : ['Unknown'];
            currentLanguage = languages[Math.floor(Math.random() * languages.length)];
            currentCountry = randomCountry.name.common;
            languageScript.textContent = `Random text in ${currentLanguage}`;
        } catch (error) {
            console.error('Error fetching language:', error);
            result.textContent = 'Error fetching language. Please try again later.';
        }
    };

    // Function to check the user's guess
    const checkGuess = () => {
        const userGuess = guessInput.value.trim().toLowerCase();
        if (userGuess === currentLanguage.toLowerCase()) {
            result.textContent = `Correct! The language is ${currentLanguage} from ${currentCountry}.`;
            result.style.color = 'green';
        } else {
            result.textContent = `Wrong! The correct answer was ${currentLanguage} from ${currentCountry}.`;
            result.style.color = 'red';
        }
        guessInput.value = '';
        fetchRandomLanguage();
    };

    // Event listener for the submit button
    submitBtn.addEventListener('click', checkGuess);

    // Event listener for the "Next" button
    nextBtn.addEventListener('click', () => {
        window.location.href = 'index3.html';
    });

    // Event listener for the "Back" button
    backBtn.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    // Fetch the first random language when the page loads
    fetchRandomLanguage();
});