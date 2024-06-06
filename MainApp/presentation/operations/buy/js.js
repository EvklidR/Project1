$(document).ready(function() {

    $(".operationsHead").addClass("selected");


    // Находим родительский элемент
    const $parentElement = $('.options');

    // Находим второго потомка и добавляем ему класс
    $parentElement.children().eq(1).addClass('selected');


    const groupList = $('.popup ul');
    const overlay = $('.overlay');
    const popup = $('.popup');

    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        var tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty')
            .text("Поступлений нет")
            .css("width", "100%")
            .css("text-align", "center");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const buy = data[i];
            const response = await fetch(`/db/getAddressStore/?store_id=${buy.idStore}`);
            if (response.ok) {
                const address = await response.json();
                const totalCost = await fetch(`/db/get_cost_of_buy/?buy_id=${buy.id}`)
                    .then(response => response.json());

                const row = $('<div>').addClass('tablerow').attr('data-buy-id', buy.id);
                const numberCell = $('<div>').addClass('tableElem t0').text(i + 1);
                const generalCostCell = $('<div>').addClass('tableElem t2').text(totalCost);
                const addressCell = $('<div>').addClass('tableElem t1').text(address);
                const dateCell = $('<div>').addClass('tableElem t2').text(buy.date);

                const actionsCell = $('<div>').addClass('tableElem t0 actions');
                const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');

                actionsCell.append(deleteIcon);
                row.append(numberCell, generalCostCell, addressCell, dateCell, actionsCell);
                tableBody.append(row);

                // Добавление обработчика клика на строку
                row.click(async function() {
                    event.stopPropagation();
                    const buyId = $(this).data('buy-id');
                    const products = await fetchBuyProducts(buyId);
                    showProductsModal(products);
                });

                deleteIcon.on('click', () => {
                    event.stopPropagation(); // Предотвращаем всплытие события

                    // Отправка запроса на сервер для удаления элемента из базы данных
                    fetch(`/db/buy/?buy_id=${buy.id}`, {
                        method: 'DELETE'
                    })
                        .then(response => {
                            row.remove();

                                                        // Проверяем, остались ли ещё строки в таблице
                            const tableRows = $('.tablerow');
                            if (tableRows.length === 1) {
                                // Если в таблице осталась только одна строка (это заголовок), добавляем сообщение о том, что складов нет
                                var emptyRow = $('<div>').addClass('tablerow');
                                var emptyCell = $('<div>').addClass('tableElem empty').text("Поступлений нет")
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
                console.error(`Ошибка при получении адреса для поступления с ID ${buy.id}`);
            }
        }
    }

    // Функция для получения информации о товарах для конкретного поступления
    async function fetchBuyProducts(buyId) {
        const response = await fetch(`/db/get_buy_products/?buy_id=${buyId}`);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Ошибка при получении информации о товарах');
        }
    }

    // Функция для отображения всплывающего окна с информацией о товарах
    function showProductsModal(products) {
        // Очистка списка групп
        groupList.empty();

        const head = $('<div>').addClass('product-item products-head');

        const nameDiv = $('<div>').addClass('product-attr');
        nameDiv.text("Наименование");
        head.append(nameDiv);

        // Product Price
        const priceDiv = $('<div>').addClass('product-attr');
        priceDiv.text("Цена, р");
        head.append(priceDiv);

        // Product Quantity
        const quantityDiv = $('<div>').addClass('product-attr');
        quantityDiv.text("Количество");
        head.append(quantityDiv);

        groupList.append(head);

        // Заполнение списка названиями товаров
        products.forEach(product => {
          const listItem = $('<div>').addClass('product-item');

          // Product Name
          const nameDiv = $('<div>').addClass('product-attr');
          nameDiv.text(product.name);
          listItem.append(nameDiv);

          // Product Price
          const priceDiv = $('<div>').addClass('product-attr');
          priceDiv.text(product.cost);
          listItem.append(priceDiv);

          // Product Quantity
          const quantityDiv = $('<div>').addClass('product-attr');
          quantityDiv.text(product.amount);
          listItem.append(quantityDiv);

          groupList.append(listItem);
        });

        // Показываем overlay и всплывающее окно
        overlay.css('display', 'block');
        popup.css('display', 'block');
    }

    // Отправка запроса на сервер для получения списка поступлений
    fetch('/db/buy')
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



    // Обработчик события клика на overlay
    overlay.on('click', function() {
        overlay.css('display', 'none');
        popup.css('display', 'none');
    });

});