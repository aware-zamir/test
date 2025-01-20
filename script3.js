document.addEventListener('DOMContentLoaded', () => {
    const foodImage = document.getElementById('food-image');
    const guessInput = document.getElementById('guess-input');
    const submitBtn = document.getElementById('submit-btn');
    const result = document.getElementById('result');
    const nextBtn = document.getElementById('index.html');
    const backBtn = document.getElementById('index2.html');

    let currentFood = '';

    // Function to fetch a random food image
    const fetchRandomFood = async () => {
        try {
            const response = await fetch('https://www.themealdb.com/api/json/v1/1/random.php');
            const data = await response.json();
            const randomFood = data.meals[0];
            currentFood = randomFood.strMeal;
            foodImage.src = randomFood.strMealThumb;
            foodImage.alt = `Image of ${currentFood}`;
        } catch (error) {
            console.error('Error fetching food:', error);
            result.textContent = 'Error fetching food. Please try again later.';
        }
    };

    // Function to check the user's guess
    const checkGuess = () => {
        const userGuess = guessInput.value.trim().toLowerCase();
        if (userGuess === currentFood.toLowerCase()) {
            result.textContent = 'Correct! Well done!';
            result.style.color = 'green';
        } else {
            result.textContent = `Wrong! The correct answer was ${currentFood}.`;
            result.style.color = 'red';
        }
        guessInput.value = '';
        fetchRandomFood();
    };

    // Event listener for the submit button
    submitBtn.addEventListener('click', checkGuess);

    // Event listener for the "Next" button
    nextBtn.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    // Event listener for the "Back" button
    backBtn.addEventListener('click', () => {
        window.location.href = 'index2.html';
    });

    // Fetch the first random food when the page loads
    fetchRandomFood();
});