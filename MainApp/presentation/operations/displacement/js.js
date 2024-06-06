(async function($){
    "use strict";

    $(".operationsHead").addClass("selected");

    // Находим родительский элемент
    const parentElement = $('.options');

    const overlay = $('.overlay');
    const popup = $('.popup');

    // Находим второго потомка и добавляем ему класс
    parentElement.children().eq(2).addClass('selected');


    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        var tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty')
            .text("Перемещений нет")
            .css("width", "100%")
            .css("text-align", "center");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const displacement = data[i];
            const response = await fetch(`/db/getAddressStore/?store_id=${displacement.idStore}`);
            const response2 = await fetch(`/db/getAddressStore/?store_id=${displacement.idStoreToMove}`);
            const response3 = await fetch(`/db/get_name_of_product/?product_id=${displacement.idProduct}`);
            if (response.ok & response2.ok & response3.ok) {
                const address = await response.json();
                const address2 = await response2.json();
                const product_name = await response3.json();

                const row = $('<div>').addClass('tablerow').attr('data-buy-id', displacement.id);
                const numberCell = $('<div>').addClass('tableElem t0').text(i + 1);
                const generalCostCell = $('<div>').addClass('tableElem t1').text(product_name);
                const addressCell = $('<div>').addClass('tableElem t1').text(address);
                const address2Cell = $('<div>').addClass('tableElem t1').text(address2);
                const amountCell = $('<div>').addClass('tableElem t2').text(displacement.amount);
                const dateCell = $('<div>').addClass('tableElem t2').text(displacement.date);

                const actionsCell = $('<div>').addClass('tableElem t0 actions');
                const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');

                actionsCell.append(deleteIcon);
                row.append(numberCell, generalCostCell, addressCell, address2Cell, amountCell, dateCell, actionsCell);
                tableBody.append(row);

                deleteIcon.on('click', () => {
                    event.stopPropagation(); // Предотвращаем всплытие события

                    // Отправка запроса на сервер для удаления элемента из базы данных
                    fetch(`/db/displacement/?displacement_id=${displacement.id}`, {
                        method: 'DELETE'
                    })
                        .then(response => {
                            row.remove();

                                                        // Проверяем, остались ли ещё строки в таблице
                            const tableRows = $('.tablerow');
                            if (tableRows.length === 1) {
                                // Если в таблице осталась только одна строка (это заголовок), добавляем сообщение о том, что складов нет
                                var emptyRow = $('<div>').addClass('tablerow');
                                var emptyCell = $('<div>').addClass('tableElem empty').text("Перемещений нет")
                                .css("width", "100%")
                                .css("text-align", "center");
                                emptyRow.append(emptyCell);
                                tableBody.append(emptyRow);
                            }

                        })
                        .catch(error => {
                            console.error('Ошибка при удалении элемента:', error);
                        });
                });

            } else {
                console.error(`Ошибка при получении адреса для поступления с ID ${displacement.id}`);
            }
        }
    }

    async function fetchData(){

        console.log("h");
        // Отправка запроса на сервер для получения списка поступлений
        fetch('/db/displacement')
        .then(function(response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка при получении списка поступлений');
            }
        })
        .then(function(data) {
            console.log(data);
            fillTable(data);
        })
        .catch(function(error) {
            console.error("Ошибка при чтении классов: ", error);
        });

    }


    // Обработчик нажатия на кнопку
    $('.batt').on('click', function () {
        overlay.css('display', 'block');
        popup.empty().css('display', 'block');

        // Создание и добавление элементов в popup
        const title = $("<div>").addClass('popup-title').text('Добавление перемещения');
        const productLabel = $('<span>').addClass('dropdown-label').text('Выберите товар:');
        const storeFromLabel = $('<span>').addClass('dropdown-label').text('Из склада:');
        const storeToLabel = $('<span>').addClass('dropdown-label').text('В склад:');
        const productList = $('<select>').addClass('dropdown').attr('id', 'product-select');
        const storeFromList = $('<select>').addClass('dropdown').attr('id', 'store-from-select');
        const storeToList = $('<select>').addClass('dropdown').attr('id', 'store-to-select');
        const quantityLabel = $('<div>').addClass('input-label').text('Количество:');
        const quantityInput = $('<input>').addClass('input-field').attr('type', 'number').attr('id', 'quantity-input');
        const productContainer = $('<div>').addClass('dropdown-container').append(productLabel, productList);
        const storeFromContainer = $('<div>').addClass('dropdown-container').append(storeFromLabel, storeFromList);
        const storeToContainer = $('<div>').addClass('dropdown-container').append(storeToLabel, storeToList);
        const quantityContainer = $('<div>').addClass('input-container').append(quantityLabel, quantityInput);

        // Получение сегодняшней даты в формате дд.мм.гггг
        const today = new Date();
        const formattedToday = ('0' + today.getDate()).slice(-2) + '.' +
            ('0' + (today.getMonth() + 1)).slice(-2) + '.' +
            today.getFullYear();

        // Создание элемента даты
        const dateContainer = $('<div>').addClass('wrap-input10 validate-input');
        const dateLabel = $('<label>').text('Дата').css('margin-right', '10px').addClass("input-label");
        const dateInput = $('<input>').addClass('input-group input100').attr({
            'type': 'text',
            'name': 'date',
            'id': 'expiry',
            'placeholder': 'Выберите дату',
            'value': formattedToday,
            'readonly': true
        });

        const focusSpan = $('<span>').addClass('focus-input100');

        const flatpickrOptions = {
            dateFormat: 'd.m.Y', // Формат даты
            disableMobile: true, // Отключить мобильный режим
            maxDate: 'today', // Ограничение максимальной даты текущим днем
            locale: {
                weekdays: {
                    shorthand: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
                    longhand: [
                        'Воскресенье',
                        'Понедельник',
                        'Вторник',
                        'Среда',
                        'Четверг',
                        'Пятница',
                        'Суббота'
                    ]
                },
                months: {
                    shorthand: [
                        'Янв',
                        'Фев',
                        'Мар',
                        'Апр',
                        'Май',
                        'Июн',
                        'Июл',
                        'Авг',
                        'Сен',
                        'Окт',
                        'Ноя',
                        'Дек'
                    ],
                    longhand: [
                        'Январь',
                        'Февраль',
                        'Март',
                        'Апрель',
                        'Май',
                        'Июнь',
                        'Июль',
                        'Август',
                        'Сентябрь',
                        'Октябрь',
                        'Ноябрь',
                        'Декабрь'
                    ]
                }
            },
            onClose: function(selectedDates, dateStr, instance) {
            }
        };

        let flatpickrInstance = null;

        dateInput.on('click', function() {
            if (flatpickrInstance) {
                flatpickrInstance.open();
            } else {
                flatpickrInstance = dateInput.flatpickr(flatpickrOptions);
                flatpickrInstance.open();
            }
        });


        dateContainer.append(dateLabel, dateInput, focusSpan);


        // Создание и добавление кнопки "Добавить"
        const addButton = $('<button>').addClass('add-button').text('Добавить');

        popup.append(
            title,
            productContainer,
            storeFromContainer,
            storeToContainer,
            quantityContainer,
            dateContainer,
            addButton
        );

        // Создание и заполнение списка продуктов
        $.get('/db/product', function (data) {
            data.forEach(function (product) {
                productList.append($('<option>').attr('value', product.id).text(product.name));
            });
        });

        // Создание и заполнение списка складов
        $.get('/db/stores', function (data) {
            const storeLists = [storeFromList, storeToList];
            storeLists.forEach(function (storeList) {
                data.forEach(function (store) {
                    storeList.append($('<option>').attr('value', store.id).text(store.name));
                });
            });
        });

        // Обработчик нажатия на кнопку "Добавить"
        addButton.on('click', async function () {
            const quantityValue = quantityInput.val();

            // Проверка, не пусто ли значение количества
            if (!quantityValue) {
                quantityInput.parent().addClass("alert-validate");
                return;
            }

            // Действия по добавлению перемещения (пример)
            const selectedProduct = productList.val();
            const selectedStoreFrom = storeFromList.val();
            const selectedStoreTo = storeToList.val();
            const selectedDate = dateInput.val();

            // Ваша логика для обработки данных, например, отправка на сервер
            const data = {
                idCompany: null,
                idWorker: null,
                created_at: null,
                idProduct: selectedProduct,
                idStore: selectedStoreFrom,
                idStoreToMove: selectedStoreTo,
                date: selectedDate,
                amount: quantityValue
            };

            console.log(data);

            fetch('/db/displacement', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(async function() {
                await fetchData();

            })
            .catch(error => {
                console.error('Ошибка при добавлении перемещения:', error);
            });

            // Закрытие модального окна после успешного добавления
            overlay.css('display', 'none');
            popup.css('display', 'none');
        });
    });


    // Обработчик закрытия модального окна при клике на overlay
    overlay.on('click', function() {
        overlay.css('display', 'none');
        popup.css('display', 'none');
    });

    await fetchData();

})(jQuery);