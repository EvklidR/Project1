$(document).ready(function() {

    $(".operationsHead").addClass("selected");


    // Находим родительский элемент
    const $parentElement = $('.options');

    // Находим второго потомка и добавляем ему класс
    $parentElement.children().eq(4).addClass('selected');


    const groupList = $('.popup ul');
    const overlay = $('.overlay');
    const popup = $('.popup');

    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        var tableBody = $('.tablebody');
        tableBody.empty();

        for (let i = 0; i < data.length; i++) {
            const inventory = data[i];
            const response = await fetch(`/db/getAddressStore/?store_id=${inventory.idStore}`);
            if (response.ok) {
                const address = await response.json();

                var row = $('<div>').addClass('tablerow').attr('data-buy-id', inventory.id);
                var numberCell = $('<div>').addClass('tableElem t0').text(i + 1);
                var addressCell = $('<div>').addClass('tableElem t1').text(address);
                var dateCell = $('<div>').addClass('tableElem t2').text(inventory.date);

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
    fetch('/db/inventory')
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