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

// Определение текущего пути URL
const currentPath = window.location.pathname;

// Функция для формирования правильной ссылки в зависимости от текущего пути URL
function generateFuelUrl(prefix, fuelName) {
    return `${prefix}${fuelName}`;
}

// Обновленная функция для получения предложений поиска и перенаправления на страницу товара с правильной ссылкой
function fetchSuggestions(query) {
    fetch(`/search-suggestions/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            suggestionsList.innerHTML = ''; // Очистить предыдущие предложения
            data.suggestions.forEach(fuelName => {
                const listItem = document.createElement('li');
                listItem.textContent = fuelName;
                suggestionsList.appendChild(listItem);

                // Добавляем обработчик события клика на каждый элемент списка предложений
                listItem.addEventListener('click', () => {
                    fetch(`/get-fuel-url/?fuel_name=${fuelName}`)
                        .then(response => response.json())
                        .then(data => {
                            // Получаем чистый URL без префикса
                            const cleanUrl = data.url;
                            // Формируем правильный префикс URL в зависимости от текущего пути
                            let prefix;
                            if (currentPath.startsWith('/pf-catalog/')) {
                                prefix = '/pf-catalog/';
                            } else if (currentPath.startsWith('/pf-home/')) {
                                prefix = '/pf-home/';
                            } else {
                                prefix = '/search/';
                            }
                            // Формируем ссылку с правильным префиксом
                            const fuelUrl = generateFuelUrl(prefix, cleanUrl);
                            // Перенаправляем пользователя на страницу с товаром, используя сформированную ссылку
                            window.location.href = fuelUrl;
                        })
                        .catch(error => {
                            console.error('Error fetching fuel URL:', error);
                        });
                });
            });
        })
        .catch(error => {
            console.error('Error fetching suggestions:', error);
        });
}
s




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
