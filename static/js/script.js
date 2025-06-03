document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelectorAll('.toggle-button');

    toggleButton.forEach(button => {
        const textBlock = button.closest('.opisanie');
        const hiddenText = textBlock.querySelector('.hidden-text');

        button.addEventListener('click', function() {
            hiddenText.classList.toggle('expanded');
            if (hiddenText.classList.contains('expanded')) {
                button.textContent = 'Скрыть';
            } else {
                button.textContent = 'Ещё';
            };
        });
    });

    const toggleMoreButtons = document.querySelectorAll('.js-more-toggle');
    const toggleHideButtons = document.querySelectorAll('.js-hide-toggle');

    toggleMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const samsungCard = this.closest('.samsung');
            if (samsungCard) {
                const compactView = samsungCard.querySelector('.phone-compact');
                const detailedView = samsungCard.querySelector('.js-detailed-info');

                if (compactView && detailedView) {
                    detailedView.style.display = 'block';
                    compactView.style.display = 'none';
                }
            }
        });
    });

    toggleHideButtons.forEach(button => {
        button.addEventListener('click', function() {
            const samsungCard = this.closest('.samsung');
            if (samsungCard) {
                const compactView = samsungCard.querySelector('.phone-compact');
                const detailedView = samsungCard.querySelector('.js-detailed-info');

                if (compactView && detailedView) {
                    detailedView.style.display = 'none';
                    compactView.style.display = 'flex';
                }
            }
        });
    });

    const detailedImages = document.querySelectorAll('.js-detailed-info .charact img');
    detailedImages.forEach(img => {
        img.addEventListener('click', function() {
            const samsungCard = this.closest('.samsung');
            if (samsungCard) {
                const compactView = samsungCard.querySelector('.phone-compact');
                const detailedView = samsungCard.querySelector('.js-detailed-info');
                if (compactView && detailedView) {
                    detailedView.style.display = 'none';
                    compactView.style.display = 'block';
                }
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like');
    async function sendLikeRequest(phoneId, isLiked) {
        const url = `/like/phone/${phoneId}?liked=${isLiked}`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log(`Лайк/дизлайк для телефона ${phoneId} успешно отправлен.`, data);
            } else {
                console.error(`Ошибка при отправке лайка/дизлайка для телефона ${phoneId}:`, response.status, response.statusText);
                currentLikeButton.classList.toggle('liked');
            }
        } catch (error) {
            console.error(`Произошла сетевая ошибка для телефона ${phoneId}:`, error);
            currentLikeButton.classList.toggle('liked');
        };
    };

    likeButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const currentLikeButton = event.currentTarget;
            currentLikeButton.classList.toggle('liked');
            const isLiked = currentLikeButton.classList.contains('liked');
            const phoneCompactDiv = currentLikeButton.closest('.phone-compact');
            const phoneId = phoneCompactDiv.dataset.phoneId;
            if (isLiked == true) {
                currentLikeButton.style.display = "block"
                currentLikeButton.style.color = "red"
            }
            if (isLiked == false) {
                currentLikeButton.style.display = "none"
            }
            if (phoneId) {
                console.log(`Клик на лайк для телефона ID: ${phoneId}. Состояние: ${isLiked ? 'Лайкнут' : 'Не лайкнут'}`);
                sendLikeRequest(phoneId, isLiked);
            } else {
                console.warn('Не удалось получить ID телефона для элемента:', phoneCompactDiv);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const addToBasketButtons = document.querySelectorAll('.add-to-basket');

    const currentUsername = getCookie('username')

    addToBasketButtons.forEach(button => {
        button.addEventListener('click', async(event) => {
            const clickedButton = event.currentTarget;

            const productContainer = clickedButton.closest('.samsung');

            if (!productContainer) {
                console.error('Не удалось найти родительский контейнер .samsung для кнопки "add to basket".');
                return;
            }

            const phoneCompactDiv = productContainer.querySelector('.phone-compact');

            if (!phoneCompactDiv) {
                console.error('Не удалось найти .phone-compact внутри контейнера .samsung.');
                return;
            }

            const phoneId = phoneCompactDiv.dataset.phoneId;

            if (!phoneId) {
                console.error('Не удалось получить data-phone-id для товара.', phoneCompactDiv);
                return;
            }

            console.log(`Попытка добавить товар ID: ${phoneId} в корзину пользователя: ${currentUsername}`);

            const url = `/add_to_basket/${currentUsername}?id=${phoneId}`;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    console.log('Ответ сервера:', data);
                    alert(`Товар ${phoneId} успешно добавлен в корзину!`);
                } else {
                    console.error('Ошибка при добавлении в корзину:', data.message || 'Неизвестная ошибка');
                    alert(`Ошибка: ${data.message || 'Не удалось добавить товар в корзину.'}`);
                }
            } catch (error) {
                console.error('Сетевая ошибка при отправке запроса:', error);
                alert('Произошла сетевая ошибка. Пожалуйста, попробуйте еще раз.');
            }
        });
    });
});