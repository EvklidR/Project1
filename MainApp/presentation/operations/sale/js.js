$(document).ready(function() {

    $(".operationsHead").addClass("selected");

        // Находим родительский элемент
    const parentElement = $('.options');
    // Находим второго потомка и добавляем ему класс
    parentElement.children().eq(0).addClass('selected');


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
            .text("Продаж нет")
            .css("width", "100%")
            .css("text-align", "center");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const sale = data[i];
            const response = await fetch(`/db/getAddressStore/?store_id=${sale.idStore}`);
            if (response.ok) {
                const address = await response.json();
                const totalCost = await fetch(`/db/get_cost_of_sale/?sale_id=${sale.id}`)
                    .then(response => response.json());

                const row = $('<div>').addClass('tablerow').attr('data-sale-id', sale.id);
                const numberCell = $('<div>').addClass('tableElem t0').text(sale.id);
                const generalCostCell = $('<div>').addClass('tableElem t2').text(totalCost);
                const addressCell = $('<div>').addClass('tableElem t1').text(address);
                const dateCell = $('<div>').addClass('tableElem t2 date').text(sale.date);
                const actionsCell = $('<div>').addClass('tableElem t0 actions');
                const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');

                actionsCell.append(deleteIcon);
                row.append(numberCell, generalCostCell, addressCell, dateCell, actionsCell);
                tableBody.append(row);

                // Добавление обработчика клика на строку
                row.click(async function() {
                    event.stopPropagation();
                    const products = await fetchBuyProducts(sale.id);
                    showProductsModal(products, sale);
                });

                deleteIcon.on('click', () => {
                    event.stopPropagation(); // Предотвращаем всплытие события

                    // Отправка запроса на сервер для удаления элемента из базы данных
                    fetch(`/db/sale/?sale_id=${sale.id}`, {
                        method: 'DELETE'
                    })
                        .then(response => {
                            row.remove();

                            // Проверяем, остались ли ещё строки в таблице
                            const tableRows = $('.tablerow');
                            if (tableRows.length === 1) {
                                // Если в таблице осталась только одна строка (это заголовок), добавляем сообщение о том, что складов нет
                                var emptyRow = $('<div>').addClass('tablerow');
                                var emptyCell = $('<div>').addClass('tableElem empty').text("Продаж нет")
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
                console.error(`Ошибка при получении адреса для поступления с ID ${sale.id}`);
            }
        }
    }


    let currentSortColumn = '';
    let currentSortOrder = 'asc';

    function parseDate(dateString) {
        const parts = dateString.split('.');
        return new Date(parts[2], parts[1] - 1, parts[0]);
    }

    function sortTable(column, type) {
        const tableRows = $('.tablerow').toArray();
        tableRows.shift(); // Удаляем первый элемент из массива

        tableRows.sort((a, b) => {
            const aValue = $(a).find(`.${column}`).text();
            const bValue = $(b).find(`.${column}`).text();

            let comparison = 0;

            if (type === 'number') {
                // Сортировка как числа
                comparison = parseFloat(aValue) - parseFloat(bValue);
            } else if (type === 'string') {
                // Сортировка как строки
                comparison = aValue.localeCompare(bValue, undefined, { numeric: true });
            } else if (type === 'date') {
                // Сортировка как даты
                const dateA = parseDate(aValue);
                const dateB = parseDate(bValue);
                comparison = dateA - dateB;
            }

            if (currentSortOrder === 'asc') {
                return comparison;
            } else {
                return -comparison;
            }
        });

        $('.tablebody').append(tableRows);
    }

    function toggleSortOrder(column) {
        if (currentSortColumn === column) {
            currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            currentSortColumn = column;
            currentSortOrder = 'asc';
        }
    }

    $('#SortByDate').on('click', function() {
        console.log("here");
        toggleSortOrder('date'); // Assuming the column class for the date is 'date'
        sortTable('date', "date");
    });

    // Функция для получения информации о товарах для конкретного поступления
    async function fetchBuyProducts(saleId) {
        const response = await fetch(`/db/get_sale_products/?sale_id=${saleId}`);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Ошибка при получении информации о товарах');
        }
    }

// Функция для отображения всплывающего окна с информацией о товарах
function showProductsModal(products, sale) {
    // Очистка списка групп
    groupList.empty();
    $(".creation-date").remove()

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

    // Return Button Header
    const returnHeader = $('<div>').css("width", "80px");
    returnHeader.text("");
    head.append(returnHeader);

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

        // Return Button
        const returnButton = $('<button>').addClass('return-button').text('Возврат');
        listItem.append(returnButton);

        // Добавляем обработчик события для кнопки "Возврат"
        returnButton.on('click', async () => {
            if (returnButton.text() === 'Возврат') {
                // Получаем возвраты для текущей продажи
                var response = await fetch(`/db/get_returns_for_sale/?sale_id=${sale.id}`);
                var returns = await response.json();

                // Проверяем, есть ли текущий товар в списке возвратов
                let currentReturn = returns.find(ret => ret.name === product.name);

                listItem.css("border-bottom", "none");
                const returnRow = $('<div>').addClass('product-item return-row').css("border-top", "none");

                const emptyNameDiv = $('<div>').addClass('product-attr').text("Возврат");
                returnRow.append(emptyNameDiv);

                const returnPriceDiv = $('<div>').addClass('product-attr');
                const returnQuantityDiv = $('<div>').addClass('product-attr');

                if (currentReturn) {
                    returnRow.attr("return_id", currentReturn.return_id);
                    // Если возврат уже существует, показываем текст вместо полей ввода
                    returnPriceDiv.text(currentReturn.cost);
                    returnQuantityDiv.text(currentReturn.amount);

                    // Заменяем кнопку "Оформить" на иконку удаления
                    const deleteIcon = $('<i>').addClass('delete-icon-return').html('&#10060;');
                    returnRow.append(returnPriceDiv);
                    returnRow.append(returnQuantityDiv);
                    returnRow.append(deleteIcon);

                    // Обработчик события для крестика удаления строки возврата
                    deleteIcon.on('click', function () {
                        event.stopPropagation(); // Предотвращаем всплытие события

                        // Получаем строку возврата, к которой относится крестик
                        const returnRow = $(this).closest('.return-row');

                        // Отправка запроса на сервер для удаления строки возврата из базы данных
                        fetch(`/db/del_return/?return_id=${returnRow.attr("return_id")}`, {
                            method: 'DELETE'
                        })
                        .then(response => {
                            // Удаляем строку возврата из DOM
                            returnRow.remove();
                            listItem.css("border-bottom", "1px solid #ccc");
                        })
                        .catch(error => {
                            console.error('Ошибка при удалении строки возврата:', error);
                        });
                    });
                } else {
                    const returnPriceInput = $('<input>').attr('type', 'number').addClass('return-input');
                    returnPriceDiv.append(returnPriceInput);

                    const returnQuantityInput = $('<input>')
                        .attr('type', 'number')
                        .attr('max', product.amount)  // Ограничение на максимальное количество
                        .addClass('return-input');
                    returnQuantityDiv.append(returnQuantityInput);

                    // Обработчик события при изменении поля ввода количества
                    returnQuantityInput.on('input', function () {
                        // Получаем текущее значение поля ввода
                        let currentValue = $(this).val();
                        // Получаем максимальное значение из атрибута max
                        let maxValue = $(this).attr('max');

                        // Проверяем, превышает ли текущее значение максимальное значение
                        if (parseInt(currentValue) > parseInt(maxValue)) {
                            // Если превышает, устанавливаем текущее значение равным максимальному
                            $(this).val(maxValue);
                        }
                    });

                    // Кнопка "Оформить"
                    const confirmButton = $('<button>').addClass('confirm-button').text('Оформить');
                    // Обработчик события для кнопки "Оформить"
                    confirmButton.on('click', async function () {
                        const returnPrice = returnPriceInput.val();
                        const returnQuantity = returnQuantityInput.val();

                        // Проверка на пустое или отрицательное значение цены и количества
                        if (returnPrice === '' || returnPrice <= 0) {
                            returnPriceInput.addClass('invalid-input');
                        } else {
                            returnPriceInput.removeClass('invalid-input');

                            if (returnQuantity === '' || returnQuantity <= 0) {
                                returnQuantityInput.addClass('invalid-input');
                            } else {
                                returnQuantityInput.removeClass('invalid-input');

                                const returnData = {
                                    idCompany: null,
                                    idWorker: null,
                                    created_at: null,
                                    date: null,
                                    idProduct: product.product_id,
                                    cost: Number(returnPrice),
                                    amount: Number(returnQuantity),
                                    idStore: sale.idStore,
                                    idSale: sale.id
                                };

                                // Заменяем поля ввода на текст
                                returnPriceDiv.empty().text(returnPrice);
                                returnQuantityDiv.empty().text(returnQuantity);

                                // Заменяем кнопку "Оформить" на иконку удаления
                                confirmButton.replaceWith($('<i>').addClass('delete-icon-return').html('&#10060;'));

                                fetch('/db/create_return', {
                                    method: 'POST',
                                    body: JSON.stringify(returnData),
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                })
                                .then(async function (response) {
                                    response = await response.json();
                                    console.log(response);
                                    returnRow.attr("return_id", response["id"]);
                                })
                                .catch(error => {
                                    console.error('Ошибка при добавлении возврата:', error);
                                });

                                // Обработчик события для крестика удаления строки возврата
                                $(".delete-icon-return").on('click', function () {
                                    event.stopPropagation(); // Предотвращаем всплытие события

                                    // Получаем строку возврата, к которой относится крестик
                                    const returnRow = $(this).closest('.return-row');

                                    // Отправка запроса на сервер для удаления строки возврата из базы данных
                                    fetch(`/db/del_return/?return_id=${returnRow.attr("return_id")}`, {
                                        method: 'DELETE'
                                    })
                                    .then(response => {
                                        // Удаляем строку возврата из DOM
                                        returnRow.remove();
                                        listItem.css("border-bottom", "1px solid #ccc");
                                        returnButton.text("Возврат")
                                    })
                                    .catch(error => {
                                        console.error('Ошибка при удалении строки возврата:', error);
                                    });
                                });
                            }
                        }
                    });

                    returnRow.append(returnPriceDiv);
                    returnRow.append(returnQuantityDiv);
                    returnRow.append(confirmButton);
                }

                listItem.after(returnRow);

                // Заменяем текст кнопки "Возврат" на "Отменить"
                returnButton.text('Отменить');
            } else {
                // Удаляем строку возврата и возвращаем текст кнопки "Возврат"
                listItem.next('.return-row').remove();
                listItem.css("border-bottom", "1px solid #ccc");
                returnButton.text('Возврат');
            }
        });

        groupList.append(listItem);
    });

    // Добавляем строку с датой создания продажи в конце списка
    const dateText = $('<div>').addClass('creation-date').text(`Дата создания записи: ${sale.created_at}`);
    groupList.after(dateText);

    // Показываем overlay и всплывающее окно
    overlay.css('display', 'block');
    popup.css('display', 'block');
}



    // Отправка запроса на сервер для получения списка продаж
    fetch('/db/sale')
        .then(function(response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Ошибка при получении списка продаж');
            }
        })
        .then(function(data) {
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