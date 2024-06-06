(async function($){
    "use strict";

    $(".prodHead").addClass("selected");

    let currentSortColumn = null;
    let currentSortOrder = 'asc';

    async function fetchData(){
        // Отправка запроса на сервер для получения списка продаж
        fetch(`/db/product/?skip=0&limit=30&search_query=${$(".search").val()}`)
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Ошибка при получении списка товаров');
                }
            })
            .then(function(data) {
                fillTable(data);
            })
            .catch(function(error) {
                console.error("Ошибка при чтении классов: ", error);
            });
    }

    async function fillTable(data) {
        var tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty').text("Товаров нет").css("width", "100%");
            emptyRow.append(emptyCell);
            tableBody.append(emptyRow);
            return; // Выходим из функции, так как нет данных для отображения
        }

        for (let i = 0; i < data.length; i++) {
            const product = data[i];

            var row = $('<div>').addClass('tablerow');
            row.on('click', function() {
                window.location.href = `/company/info?id=${product.id}`;
            });
            var nameCell = $('<div>').addClass('tableElem t0 name').text(product.name);

            var selectedValue = $("#months").val();

            var response = await fetch(`/db/get_total_amount_of_sale?product_id=${product.id}&period=${selectedValue}`);
            var value = await response.json();

            var amountSale = $('<div>').addClass('tableElem t1 sale').text(value);

            var response = await fetch(`/db/get_total_amount_of_buy?product_id=${product.id}&period=${selectedValue}`);
            var value = await response.json();

            var amountBuy = $('<div>').addClass('tableElem t1 buy').text(value);

            response = await fetch(`/db/get_total_amount_on_store?product_id=${product.id}`);
            value = await response.json();

            var amountOnStore = $('<div>').addClass('tableElem t2 onStore').text(value);

            row.append(nameCell, amountSale, amountBuy, amountOnStore);
            tableBody.append(row);
        }
    }


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

    $('#sortByName').on('click', function() {
        toggleSortOrder('t0');
        sortTable('name', "string");
    });

    $('#sortBySales').on('click', function() {
        toggleSortOrder('t1');
        sortTable('sale', "number");
    });

    $('#sortByBuys').on('click', function() {
        toggleSortOrder('t1');
        sortTable('buy', "number");
    });

    $('#sortByStock').on('click', function() {
        toggleSortOrder('t2');
        sortTable('onStore', "number");
    });

    $("#months").on("change", async function() {
        var selectedValue = $(this).val();
        if (selectedValue < 1 || selectedValue > 12) {
            $(this).val('');
        } else {
            await fetchData();
        }
    });

    $(".search").on("input", async function() {
        await fetchData();
    });

    await fetchData();

})(jQuery);
