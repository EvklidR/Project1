(async function($){
    "use strict";

    $(".prodHead").addClass("selected");


    async function fillTable(data) {
        var selectedValue = $("#months").val();

        var tableBody = $('.tablebody');
        tableBody.empty();

        if (data.length === 0) {
            // Если данных нет, добавляем строку "товаров нет" на всю строку
            var emptyRow = $('<div>').addClass('tablerow');
            var emptyCell = $('<div>').addClass('tableElem empty').text("Товаров нет")
            .css("width", "100%")
            .css("text-align", "center");
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
            var nameCell = $('<div>').addClass('tableElem t0').text(product.name);

            var response = await fetch(`/db/do_ABC_analysis?period=${selectedValue}`);
            var value = await response.json();
console.log(value);
            var amountSale = $('<div>').addClass('tableElem t1').text(value[product.id]["revenue_percent"]);


            var amountOnStore = $('<div>').addClass('tableElem t1').text(value[product.id]["revenue"]);

            var predictCount = $('<div>').addClass('tableElem t1').text(value[product.id]["category"]);

            row.append(nameCell, amountSale, amountOnStore, predictCount);
            tableBody.append(row);

        }
    }

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

    $(".search").on("input", async function() {

        await fetchData();

    });

    await fetchData();

})(jQuery);