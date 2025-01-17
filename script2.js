document.addEventListener('DOMContentLoaded', () => {
    // Dynamic greeting based on the time of day
    const greetingElement = document.createElement('h3');
    const currentHour = new Date().getHours();
    let greetingMessage;

    if (currentHour < 12) {
        greetingMessage = 'Good Morning!';
    } else if (currentHour < 18) {
        greetingMessage = 'Good Afternoon!';
    } else {
        greetingMessage = 'Good Evening!';
    }

    greetingElement.textContent = greetingMessage;
    document.querySelector('.content-section').prepend(greetingElement);

    // Form submission
    const form = document.createElement('form');
    form.innerHTML = `
        <label for="nameInput">Enter your name:</label>
        <input type="text" id="nameInput" name="name" required>
        <button type="submit">Submit</button>
    `;
    document.querySelector('.content-section').appendChild(form);

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const name = document.getElementById('nameInput').value.trim();
        if (name) {
            alert(`Hello, ${name}! Welcome to Page 2.`);
        }
    });

    // Random quote generator
    const quoteButton = document.createElement('button');
    quoteButton.textContent = 'Get a Random Quote';
    document.querySelector('.content-section').appendChild(quoteButton);

    const quoteDisplay = document.createElement('p');
    quoteDisplay.className = 'quote-display';
    document.querySelector('.content-section').appendChild(quoteDisplay);

    quoteButton.addEventListener('click', async () => {
        quoteDisplay.textContent = 'Fetching a random quote...';
        try {
            const response = await fetch('https://api.quotable.io/random');
            if (!response.ok) {
                throw new Error('Failed to fetch a quote');
            }
            const data = await response.json();
            quoteDisplay.textContent = `"${data.content}" - ${data.author}`;
        } catch (error) {
            quoteDisplay.textContent = 'Could not fetch a quote. Please try again later.';
        }
    });

    // To-do list
    const todoSection = document.createElement('section');
    todoSection.className = 'todo-section';
    todoSection.innerHTML = `
        <h2>To-Do List</h2>
        <form id="todoForm">
            <input type="text" id="todoInput" placeholder="Add a new task" required>
            <button type="submit">Add</button>
        </form>
        <ul id="todoList"></ul>
    `;
    document.querySelector('.content-section').appendChild(todoSection);

    const todoForm = document.getElementById('todoForm');
    const todoInput = document.getElementById('todoInput');
    const todoList = document.getElementById('todoList');

    todoForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const task = todoInput.value.trim();
        if (task) {
            const listItem = document.createElement('li');
            listItem.textContent = task;
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', () => {
                todoList.removeChild(listItem);
            });
            listItem.appendChild(deleteButton);
            todoList.appendChild(listItem);
            todoInput.value = '';
        }
    });

    // Weather fetcher
    const weatherSection = document.createElement('section');
    weatherSection.className = 'weather-section';
    weatherSection.innerHTML = `
        <h2>Weather</h2>
        <form id="weatherForm">
            <input type="text" id="cityInput" placeholder="Enter city name" required>
            <button type="submit">Get Weather</button>
        </form>
        <div id="weatherDisplay"></div>
    `;
    document.querySelector('.content-section').appendChild(weatherSection);

    const weatherForm = document.getElementById('weatherForm');
    const cityInput = document.getElementById('cityInput');
    const weatherDisplay = document.getElementById('weatherDisplay');

    weatherForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const city = cityInput.value.trim();
        if (city) {
            weatherDisplay.textContent = 'Fetching weather data...';
            try {
                const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=YOUR_API_KEY&units=metric`);
                if (!response.ok) {
                    throw new Error('City not found');
                }
                const data = await response.json();
                weatherDisplay.innerHTML = `
                    <p><strong>City:</strong> ${data.name}</p>
                    <p><strong>Temperature:</strong> ${data.main.temp}°C</p>
                    <p><strong>Weather:</strong> ${data.weather[0].description}</p>
                `;
            } catch (error) {
                weatherDisplay.textContent = 'Could not fetch weather data. Please try again later.';
            }
        }
    });

    // Add some styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .content-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }
        form input {
            padding: 0.5rem;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        form button {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            background-color: #4caf50;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        form button:hover {
            background-color: #388e3c;
        }
        .quote-display, .fact-display, .weather-display {
            font-size: 1.2rem;
            color: #333;
            text-align: center;
            max-width: 600px;
        }
        .todo-section {
            width: 100%;
            max-width: 600px;
        }
        .todo-section ul {
            list-style: none;
            padding: 0;
        }
        .todo-section li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem;
            border-bottom: 1px solid #ccc;
        }
        .todo-section li button {
            padding: 0.25rem 0.5rem;
            border: none;
            border-radius: 5px;
            background-color: #ff6f61;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .todo-section li button:hover {
            background-color: #e53935;
        }
    `;
    document.head.appendChild(style);
});