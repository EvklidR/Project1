$(document).ready(function() {

    $(".operationsHead").addClass("selected");


    // Находим родительский элемент
    const parentElement = $('.options');

    // Находим второго потомка и добавляем ему класс
    parentElement.children().eq(3).addClass('selected');


    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        var tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty')
            .text("Возвратов нет")
            .css("width", "100%")
            .css("text-align", "center");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const cur_return = data[i];
            const response = await fetch(`/db/getAddressStore/?store_id=${cur_return.idStore}`);
            const response2 = await fetch(`/db/get_name_of_product/?product_id=${cur_return.idProduct}`);

            if (response.ok && response2.ok) {
                const address = await response.json();
                const product = await response2.json();

                const row = $('<div>').addClass('tablerow').attr('data-buy-id', cur_return.id);
                const numberCell = $('<div>').addClass('tableElem t1').text(product);
                const generalCostCell = $('<div>').addClass('tableElem t1').text(address);
                const costCell = $('<div>').addClass('tableElem t2').text(cur_return.cost);
                const addressCell = $('<div>').addClass('tableElem t2').text(cur_return.amount);
                const saleCell = $('<div>').addClass('tableElem t2').text(cur_return.idSale);

                // Создание выпадающего списка для статуса
                const statusCell = $('<div>').addClass('tableElem t1 status');
                const statusSelect = $('<select>').addClass('status-select');
                const statuses = ["Подана заявка", "Заявка отклонена", "Заявка одобрена", "Товар возвращен"];

                statuses.forEach(status => {
                    const option = $('<option>').val(status).text(status);
                    if (status === cur_return.status) {
                        option.attr('selected', 'selected');
                    }
                    statusSelect.append(option);
                });

                statusSelect.on('change', async function () {
                    const newStatus = $(this).val();
                    const Id = cur_return.id;

                    try {
                        const response = await fetch(`/db/update_return/?return_id=${Id}&status=${newStatus}`, {
                            method: 'PATCH',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });

                        if (!response.ok) {
                            throw new Error('Ошибка при обновлении статуса');
                        }

                        const responseData = await response.json();
                        console.log(responseData);
                    } catch (error) {
                        console.error('Ошибка при обновлении статуса:', error);
                        alert('Произошла ошибка при обновлении статуса');
                        // Восстановить старый статус, если произошла ошибка
                        $(this).val(user.status);
                    }
                });

                statusCell.append(statusSelect)

                const dateCell = $('<div>').addClass('tableElem t2').text(cur_return.date);

                const actionsCell = $('<div>').addClass('tableElem t0 actions');
                const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');



                deleteIcon.on('click', () => {
                    event.stopPropagation(); // Предотвращаем всплытие события

                    // Отправка запроса на сервер для удаления элемента из базы данных
                    fetch(`/db/del_return/?return_id=${cur_return.id}`, {
                        method: 'DELETE'
                    })
                        .then(response => {
                            row.remove();
                                                        // Проверяем, остались ли ещё строки в таблице
                            const tableRows = $('.tablerow');
                            if (tableRows.length === 1) {
                                // Если в таблице осталась только одна строка (это заголовок), добавляем сообщение о том, что складов нет
                                var emptyRow = $('<div>').addClass('tablerow');
                                var emptyCell = $('<div>').addClass('tableElem empty').text("Возвратов нет")
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

                actionsCell.append(deleteIcon);
                row.append(numberCell, generalCostCell, costCell, addressCell, saleCell, statusCell, dateCell, actionsCell);
                tableBody.append(row);
            } else {
                console.error(`Ошибка при получении адреса для поступления с ID ${buy.id}`);
            }
        }
    }

    // Обработчик события изменения значения в списке "Со статусом"
    $('#sort').on('change', function() {
        const selectedStatus = $(this).val(); // Получаем выбранный статус

        // Получаем все строки таблицы
        var tableRows = $('.tablerow');
        tableRows.splice(0, 1);

        console.log(tableRows);

        // Фильтруем строки по выбранному статусу
        tableRows.each(function() {
            const row = $(this);
            const statusCell = row.find('.status .status-select option:selected'); // Предполагаем, что ячейка со статусом имеет класс .tableElem.t1
console.log(statusCell);
            if (statusCell.text() === selectedStatus || selectedStatus === '') {
                // Если статус строки совпадает с выбранным статусом или выбран "Все", то показываем строку
                row.show();
            } else {
                // Если статус строки не совпадает с выбранным статусом, то скрываем строку
                row.hide();
            }
        });
    });

    // Отправка запроса на сервер для получения списка поступлений
    fetch('/db/get_return')
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

});