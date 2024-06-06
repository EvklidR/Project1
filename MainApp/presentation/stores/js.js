(async function($){
    "use strict";

    $(".storesHead").addClass("selected");
    let currentRow = null;

    let currentSortColumn = null;
    let currentSortOrder = 'asc';


    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        const tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty')
            .text("Складов нет")
            .css("width", "100%")
            .css("text-align", "center");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const store = data[i];

            const row = $('<div>').addClass('tablerow');
            const addressCell = $('<div>').addClass('tableElem t1 address').text(store.name);

            var selectedValue = $("#months").val();

            const [receivedValue, shippedValue, totalQuantity] = await Promise.all([
                fetch(`/db/get_amount_buy_of_store/?store_id=${store.id}&period=${selectedValue}`).then(response => response.json()),
                fetch(`/db/get_amount_sale_of_store/?store_id=${store.id}&period=${selectedValue}`).then(response => response.json()),
                fetch(`/db/get_amount_products_on_store/?store_id=${store.id}&period=${selectedValue}`).then(response => response.json())
            ]);

            const receivedCell = $('<div>').addClass('tableElem t2 buys').text(receivedValue);
            const shippedCell = $('<div>').addClass('tableElem t2 sales').text(shippedValue);
            const totalQuantityCell = $('<div>').addClass('tableElem t2 onStore').text(totalQuantity);

            // Создание иконок редактирования и удаления
            const actionsCell = $('<div>').addClass('tableElem t2 actions');
            const editIcon = $('<i>').addClass('fa fa-pencil edit-icon');
            const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');

            // Обработчик события для иконки редактирования
            editIcon.on('click', () => {
                currentRow = row; // Сохраняем текущую редактируемую строку
                $('#editStoreAddress').val(store.name);
                $('#editStoreId').val(store.id);
                $('#editStoreType').val(store.type);
                $('.overlay, .edit-popup').css('display', 'block');
            });

            // Обработчик события для иконки удаления (добавьте вашу логику удаления здесь)
            deleteIcon.on('click', () => {
                event.stopPropagation(); // Предотвращаем всплытие события

                // Отправка запроса на сервер для удаления элемента из базы данных
                fetch(`/db/stores/?store_id=${store.id}`, {
                    method: 'DELETE'
                })
                    .then(response => {
                        row.remove();

                        // Проверяем, остались ли ещё строки в таблице
                        const tableRows = $('.tablerow');
                        if (tableRows.length === 1) {
                            // Если в таблице осталась только одна строка (это заголовок), добавляем сообщение о том, что складов нет
                            var emptyRow = $('<div>').addClass('tablerow');
                            var emptyCell = $('<div>').addClass('tableElem empty').text("Складов нет")
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

            actionsCell.append(editIcon, deleteIcon);
            row.append(addressCell, receivedCell, shippedCell, totalQuantityCell, actionsCell);
            tableBody.append(row);
        }
    }

    async function fetchData(){
    // Отправка запроса на сервер для получения списка складов
        fetch(`/db/stores/?skip=0&limit=30&search_query=${$(".search").val()}`)
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Ошибка при получении списка складов');
                }
            })
            .then(function(data) {
                fillTable(data);
            })
            .catch(function(error) {
                console.error("Ошибка при чтении классов: ", error);
            });
    }

        // Добавление обработчика события change для списка
    $("#months").on("change", async function() {
        // Получение выбранного значения из списка
        var selectedValue = $(this).val();

        // Проверка выбранного значения и выполнение соответствующих действий
        if (selectedValue < 1 || selectedValue > 12) {
            $(this).val('');
        } else {
            await fetchData();
        }
    });


    function sortTable(column, type) {
        const tableRows = $('.tablerow').toArray();
        tableRows.shift(); // Удаляем первый элемент из массива

        tableRows.sort((a, b) => {
        console.log(a, b);
            const aValue = $(a).find(`.${column}`).text();
            const bValue = $(b).find(`.${column}`).text();

            let comparison = 0;

            if (type === 'number') {
                // Сортировка как числа
                comparison = parseFloat(aValue) - parseFloat(bValue);
            } else if (type === 'string') {
                // Сортировка как строки
                comparison = aValue.localeCompare(bValue, undefined, { numeric: true });
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

    $('#address').on('click', function() {
        toggleSortOrder('address');
        sortTable('address', "string");
    });

    $('#sales').on('click', function() {
        toggleSortOrder('sales');
        sortTable('sales', "number");
    });

    $('#buys').on('click', function() {
        toggleSortOrder('buys');
        sortTable('buys', "number");
    });

    $('#onStore').on('click', function() {
        toggleSortOrder('onStore');
        sortTable('onStore', "number");
    });


    $(".search").on("input", async function() {

        await fetchData();

    });
    const overlay = $('.overlay');
    const editPopup = $('.edit-popup');

    // Закрытие модального окна при клике на overlay
    overlay.on('click', function() {
        overlay.css('display', 'none');
        editPopup.css('display', 'none');
    });

    // Сохранение изменений при редактировании
    $('#editForm').on('submit', async function(event) {
        event.preventDefault();
        const data = {
            id: $('#editStoreId').val(),
            name: $('#editStoreAddress').val(),
            type: $('#editStoreType').val(),
            idCompany: null
        }

        const response = await fetch('/db/stores', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        console.log(responseData);

        // Обновление адреса склада в текущей строке
        if (currentRow) {
            currentRow.find('.address').text($('#editStoreAddress').val());
        }

        overlay.css('display', 'none');
        editPopup.css('display', 'none');
    });

    await fetchData();

})(jQuery);