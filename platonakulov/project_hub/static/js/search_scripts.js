// JavaScript код
const inputField = document.getElementById('inputField');
const suggestionsContainer = document.getElementById('suggestions-container');
const suggestionsList = document.getElementById('suggestions-list');

// Функция для обработки ввода в поле поиска
function handleInput(event) {
    const query = event.target.value;
    if (query.length > 0) {
        fetchSuggestions(query);
        suggestionsContainer.style.display = 'block';
    } else {
        suggestionsContainer.style.display = 'none';
    }
}

// Пример вывода последних 5 прошлых запросов
const previousQueries = ['1', '2', '3', '4', '5']; // Это ваше тестовое значение, которое в дальнейшем заменится на реальные данные из базы данных
previousQueries.forEach(fuelId => {
    const listItem = document.createElement('li');
    listItem.textContent = fuelId;
    suggestionsList.appendChild(listItem);

    // Добавляем обработчик события клика на каждый элемент списка предложений
    listItem.addEventListener('click', () => {
        // Перенаправляем пользователя на страницу с товаром, используя fuel_id
        window.location.href = `http://127.0.0.1:8000/fuels/${fuelId}/`;
    });
});

function fetchSuggestions(query) {
    fetch(`/search-suggestions/?query=${query}`)
    .then(response => response.json())
    .then(data => {
        suggestionsList.innerHTML = ''; // Очистить предыдущие предложения
        data.suggestions.forEach(fuelId => {
            const listItem = document.createElement('li');
            listItem.textContent = fuelId;
            suggestionsList.appendChild(listItem);

            // Добавляем обработчик события клика на каждый элемент списка предложений
            listItem.addEventListener('click', () => {
                // Перенаправляем пользователя на страницу с товаром, используя fuel_id
                window.location.href = `http://127.0.0.1:8000/fuels/${fuelId}/`;
            });
        });
    })
    .catch(error => {
        console.error('Error fetching suggestions:', error);
    });
}

// Функция прокрутки вверх
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scrollBtn").style.display = "block";
    } else {
        document.getElementById("scrollBtn").style.display = "none";
    }
}

function scrollToTop() {
    document.body.scrollTop = 0; // Для Safari
    document.documentElement.scrollTop = 0; // Для Chrome, Firefox, IE и Opera
}

