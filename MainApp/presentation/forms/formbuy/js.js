(async function($){
    "use strict"

    const overlay = $('.overlay');
    const popup = $('.popup');
    const popupStore = $('.popup-store');
    const selectButton = $('.select-button');
    const chooseButton = $('.choose-button');
    const chooseButtonStore = $('.choose-button-store');
    const groupList = $('.popup ul');
    const groupListStore = $('.popup-store ul');
    const addIcon = $('.add-icon');
    const costInput = $('.cost');
    const amountInput = $('.amount');
    const product = $(".product-name");
    const selectButtonStore = $('.select-button-store');


    $('.login100-form-sale').submit(function(event) {
        event.preventDefault();

        var input=$('.validate-input .input100');

        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        // Проверка, были ли добавлены столбцы в таблицу
        var tableRows = $(".product-table tbody tr").length;
        if (tableRows === 0) {
            // Если нет добавленных столбцов, показать ошибку
            showValidate($('.select-button'));
            check = false;
        }


        if (check) {
            const date = $('[name="date"]').val();
            const idStore = Number($('input[name="store"]').attr("id"));
            console.log(idStore);
            console.log($('input[name="store"]'))
            const productArray = [];

            $('.product-table tbody tr').each(function() {
                const nameCell = $(this).find('td:nth-child(1)');
                const costCell = $(this).find('td:nth-child(2)');
                const amountCell = $(this).find('td:nth-child(3)');

                const product = {
                    name: nameCell.text().trim(),
                    cost: parseInt(costCell.text()),
                    amount: parseInt(amountCell.text())
                };

                productArray.push(product);
            });

            const data = {
              buy: {
                idCompany: null,
                idWorker: null,
                created_at: null,
                idStore: idStore,
                date: date
              },
              info: productArray
            };

            console.log(data);

            fetch('/db/buy', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    window.location.href = '/company/buy';
                })
                .catch(error => {
                    console.error('Ошибка при добавлении поступления:', error);
                });
        }
    });

      // Создаем массив для хранения добавленных товаров
    let addedProducts = [];

    // Обработчик события для кнопки "Добавить"
    chooseButton.on('click', function() {
        const selectedValue = groupList.find('li.selected .product-name');
        const cost = costInput.val().trim();
        const amount = amountInput.val().trim();

        if (selectedValue !== '' && cost !== '' && amount !== '') {
            const productName = selectedValue.text().trim();

            // Проверяем, был ли этот товар уже добавлен
            if (!addedProducts.includes(productName)) {
                const row = $('<tr>');
                const productNameCell = $('<td>').text(productName);
                const costCell = $('<td>').text(cost);
                const amountCell = $('<td>').text(amount);
                const actionsCell = $('<td>').append($('<span>').html('&#128465;').addClass('delete-icon').css('cursor', 'pointer'));

                row.append(productNameCell, costCell, amountCell, actionsCell);
                $('.product-table tbody').append(row);

                // Добавляем обработчик события для иконки удаления
                actionsCell.on('click', '.delete-icon', function() {
                    const rowIndex = $(this).closest('tr').index();
                    addedProducts.splice(rowIndex, 1);
                    $(this).closest('tr').remove();
                });

                // Добавляем товар в массив добавленных товаров
                addedProducts.push(productName);

                overlay.css('display', 'none');
                popup.css('display', 'none');

                groupList.find('li.selected').removeClass('selected');
                updateChooseButtonState();
            } else {
                // Если товар уже был добавлен, можно вывести сообщение или предпринять другие действия
                console.log(`Товар "${productName}" уже был добавлен.`);
            }
        }
    });

    // Обработчик события для кнопки "Добавить"
    chooseButtonStore.on('click', function() {

        // Получаем выбранный элемент списка
        const selectedValue = groupListStore.find('li.selected .store-name');

        // Подставляем выбранное значение в поле "group"
        $('input[name="store"]').val(selectedValue.text().trim());

        $('input[name="store"]').attr("id", selectedValue.attr('class').split(' ')[1]);

        // Сбрасываем выбранный элемент и деактивируем кнопку "Выбрать"
        chooseButtonStore.addClass('disabled');


        overlay.css('display', 'none');
        popupStore.css('display', 'none');
    });

    // Обработчик события для кнопки "Выбрать"
    selectButton.on('click', function() {
        hideValidate(selectButton);
        $(".alert").css("display", "none");
        costInput.val("");
        amountInput.val("");

        // Отправка запроса на сервер для получения списка товаров
        fetch('/db/product')
            .then(response => response.json())
            .then(data => {
                // Очистка списка групп
                groupList.empty();

                // Заполнение списка названиями групп и иконками корзины
                data.forEach(product => {

                        // Проверяем, был ли этот товар уже добавлен
                        if (!addedProducts.includes(product.name)) {
                            const listItem = $('<li>');
                            const productName = $('<span>').addClass('product-name').text(product.name);
                            listItem.append(productName);
                            groupList.append(listItem);
                        }
                });

                // Показываем overlay и всплывающее окно
                overlay.css('display', 'block');
                popup.css('display', 'block');
            })
            .catch(error => {
                console.error('Ошибка при получении списка групп:', error);
            });
    });


    // Обработчик события для кнопки "Выбрать"
    selectButtonStore.on('click', function() {
        hideValidate($('.input-store'));

           // Отправка запроса на сервер для получения списка групп
        fetch('/db/stores')
            .then(response => response.json())
            .then(data => {
                // Очистка списка групп
                groupListStore.empty();

                // Заполнение списка названиями групп и иконками корзины
                data.forEach(store => {
                    const listItem = $('<li>');
                    const groupName = $('<span>').addClass('store-name').text(store.name);
                    groupName.addClass(String(store.id));
                    listItem.append(groupName);
                    groupListStore.append(listItem);
                });

                // Показываем overlay и всплывающее окно
                overlay.css('display', 'block');
                popupStore.css('display', 'block');
            })
            .catch(error => {
                console.error('Ошибка при получении списка cкладов:', error);
            });
    });

    // Обработчик события для выбора пункта из меню в блоке popup
    groupList.on('click', 'li', function() {
        // Удаляем класс "selected" у всех элементов списка
        groupList.find('li').removeClass('selected');
        // Добавляем класс "selected" к выбранному элементу списка
        $(this).addClass('selected');
        updateChooseButtonState();
    });

    // Обработчик события для выбора пункта из меню в блоке popup
    groupListStore.on('click', 'li', function() {
        // Удаляем класс "selected" у всех элементов списка
        groupListStore.find('li').removeClass('selected');
        // Добавляем класс "selected" к выбранному элементу списка
        $(this).addClass('selected');
        chooseButtonStore.removeClass('disabled');
    });

    // Обработчик события для поля ввода "Цена"
    costInput.on('input', updateChooseButtonState);

    // Обработчик события для поля ввода "Количество"
    amountInput.on('input', updateChooseButtonState);

    // Функция для обновления состояния кнопки "Добавить"
    function updateChooseButtonState() {
        const selectedValue = groupList.find('li.selected .product-name').text().trim();
        const cost = costInput.val().trim();
        const amount = amountInput.val().trim();

        if (selectedValue !== '' && cost !== '' && amount !== '') {
            chooseButton.removeClass('disabled');
            chooseButton.prop('disabled', false);
        } else {
            chooseButton.addClass('disabled');
            chooseButton.prop('disabled', true);
        }
    }


    // Обработчик события клика на overlay
    overlay.on('click', function() {
        // Скрываем overlay и всплывающее окно
        overlay.css('display', 'none');
        popup.css('display', 'none');
        popupStore.css('display', 'none');
        chooseButton.addClass('disabled');
        chooseButtonStore.addClass('disabled');
    });

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
            hideValidate(this);
         });
    });


    function validate(input){
        if($(input).val().trim()==''){
            return false;
        }
    }

    function showValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).addClass('alert-validate');}

    function hideValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }



    const expiryInput = $('#expiry');
    const calendarButton = $('.calendar-button');
    const clearButton = $('.clear-button');

    const flatpickrOptions = {
        dateFormat: 'd.m.Y', // Формат даты
        disableMobile: true,// Отключить мобильный режим
        maxDate: 'today',
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
            // Здесь можно выполнить дополнительные действия после выбора даты
        }
    };

    let flatpickrInstance = null;

    // Открытие календаря по клику на кнопку
    calendarButton.html('<i class="far fa-calendar-alt"></i>');

    calendarButton.on('click', function() {
        hideValidate($('.input100'));
        if (flatpickrInstance) {
            flatpickrInstance.open();
        } else {
            flatpickrInstance = expiryInput.flatpickr(flatpickrOptions);
            flatpickrInstance.open();
        }
    });

})(jQuery);