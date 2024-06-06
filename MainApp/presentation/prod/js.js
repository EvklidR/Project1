(async function($){
    "use strict";

    let salesChart; // Переменная для хранения объекта графика
    let isForecastMode = false; // Переменная для отслеживания режима отображения (аналитика/прогноз)

    const productId = $(".title").attr("id"); // Получаем ID товара из элемента с классом "title"

    function getMonthlySalesData(productId, period) {
        return $.get(`/db/get_monthly_sale?product_id=${productId}&period=${period}`);
    }

    function getMonthlyBuysData(productId, period) {
        return $.get(`/db/get_monthly_buys?product_id=${productId}&period=${period}`);
    }

    function createHistogram(monthlySales, monthlyBuys) {
        const labels = Object.keys(monthlySales).map(month => {
            const [year, monthNumber] = month.split('-');
            return `${monthNumber}.${year}`;
        });

        const salesCounts = Object.values(monthlySales);
        const buysCounts = Object.values(monthlyBuys);

        if (salesChart) {
            salesChart.destroy(); // Уничтожаем предыдущий график перед созданием нового
        }

        const ctx = document.getElementById('salesChart').getContext('2d');
        salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Количество продаж',
                        data: salesCounts,
                        backgroundColor: 'rgba(255, 165, 0, 0.2)', // Оранжевый цвет столбцов
                        borderColor: 'rgba(255, 165, 0, 1)', // Оранжевый цвет границ столбцов
                        borderWidth: 1
                    },
                    {
                        label: 'Количество поступлений',
                        data: buysCounts,
                        backgroundColor: 'rgba(0, 0, 255, 0.2)', // Синий цвет столбцов
                        borderColor: 'rgba(0, 0, 255, 1)', // Синий цвет границ столбцов
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Месяцы',
                            color: '#000' // Черный цвет текста на оси X
                        },
                        ticks: {
                            color: '#000' // Черный цвет меток на оси X
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Количество',
                            color: '#000' // Черный цвет текста на оси Y
                        },
                        ticks: {
                            color: '#000' // Черный цвет меток на оси Y
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function updateChartWithForecast(forecast) {
        // Создаем массив с датами для следующих трех месяцев
        const today = new Date();
        const forecastDates = [];
        for (let i = 0; i < 90; i++) {
            const futureDate = new Date(today);
            futureDate.setDate(today.getDate() + i + 1); // Добавляем дни к текущей дате
            const month = (futureDate.getMonth() + 1).toString().padStart(2, '0');
            const day = futureDate.getDate().toString().padStart(2, '0');
            forecastDates.push(`${day}.${month}.${futureDate.getFullYear()}`);
        }

        const forecastData = forecast.map((value, index) => ({
            x: forecastDates[index],
            y: value
        }));

        // Обновляем график с новыми данными прогноза
        if (salesChart) {
            salesChart.destroy();
        }

        const ctx = document.getElementById('salesChart').getContext('2d');
        salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: forecastDates,
                datasets: [
                    {
                        label: 'Прогноз продаж',
                        data: forecastData.map(d => d.y),
                        backgroundColor: 'rgba(0, 255, 0, 0.2)', // Зеленый цвет столбцов
                        borderColor: 'rgba(0, 255, 0, 1)', // Зеленый цвет границ столбцов
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Дни',
                            color: '#000' // Черный цвет текста на оси X
                        },
                        ticks: {
                            color: '#000' // Черный цвет меток на оси X
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Количество',
                            color: '#000' // Черный цвет текста на оси Y
                        },
                        ticks: {
                            color: '#000' // Черный цвет меток на оси Y
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }

    $('#months').on('change', async function() {
        if (!isForecastMode) {
            const months = parseInt($(this).val());
            $.when(getMonthlySalesData(productId, months), getMonthlyBuysData(productId, months))
            .done(function(salesResponse, buysResponse) {
                const monthlySales = salesResponse[0];
                const monthlyBuys = buysResponse[0];
                createHistogram(monthlySales, monthlyBuys);
            }).fail(function(error) {
                console.error('Error fetching data:', error);
            });
            await getData();
        }
    });

    // Initial load with default period
    var initialPeriod = $('#months').val();

    $.when(getMonthlySalesData(productId, initialPeriod), getMonthlyBuysData(productId, initialPeriod))
    .done(function(salesResponse, buysResponse) {
        const monthlySales = salesResponse[0];
        const monthlyBuys = buysResponse[0];
        createHistogram(monthlySales, monthlyBuys);
    }).fail(function(error) {
        console.error('Error fetching data:', error);
    });

    async function getData() {
        initialPeriod = $('#months').val();
        var data = {};
        await fetch(`/db/do_ABC_analysis/?period=${initialPeriod}`)
        .then(async function(response){
            response = await response.json()
            data["abc_category"] = response[productId].category;
            data["total_revenue"] = response[productId].revenue;
            data["revenue_percentage"] = response[productId].revenue_percent;
            data["cumulative_revenue_percentage"] = response[productId].cumulative_percent;
        });

        await fetch(`/db/get_total_amount_on_store?product_id=${productId}`)
        .then(async function(response){
            data["current_quantity"] = await response.json();
        });

        await fetch(`/db/get_total_amount_of_sale?product_id=${productId}&period=${initialPeriod}`)
        .then(async function(response){
            var amount = await response.json();
            if (amount != 0){
                data["average_sale_price"] = (data.total_revenue / amount).toFixed(2);
            } else data["average_sale_price"] = 0;
        });

        await fetch(`/db/get_total_summ_of_buys/?product_id=${productId}&period=${initialPeriod}`)
        .then(async function(response){

            await fetch(`/db/get_total_amount_of_buy?product_id=${productId}&period=${initialPeriod}`)
            .then(async function(response2){
                var amount = await response2.json();
                var summ = await response.json();
                if (amount != 0){
                    data["average_buy_price"] = (summ/amount).toFixed(2);
                } else data["average_buy_price"] = 0;
            })

        });

        await fetch(`/db/get_turnover?product_id=${productId}&period=${initialPeriod}`)
        .then(async function(response){
            var times = await response.json();

            data["turnover"] = times;

        });

        console.log(data);
        fillData(data);
    }

    function fillData(data){
        $('#abc_category').text(data.abc_category);
        $('#total_revenue').text(data.total_revenue);
        $('#revenue_percentage').text(data.revenue_percentage);
        $('#cumulative_revenue_percentage').text(data.cumulative_revenue_percentage);
        $('#current_quantity').text(data.current_quantity);
        $('#average_sale_price').text(data.average_sale_price);
        $('#average_buy_price').text(data.average_buy_price);
        $('#turnover').text(data.turnover);
    }

    await getData();

    $(".del").on("click", () => {
        event.stopPropagation();

        fetch(`/db/product/?product_id=${productId}`, {
            method: 'DELETE'
        })
        .then(async function(response) {
            window.location.href = '/company/company';
        });
    });

    $(".update").on("click", () => {
        window.location.href = `/company/upProd?id=${productId}`;
    });

    function toggleLoadingSpinner() {
        $(".forecast-button").toggleClass("loading");
    }

    async function fetchDataAndUpdateChart() {
         // Показываем иконку загрузки
        const months = parseInt($('#months').val());
        let response;
        try {
            if (!isForecastMode) {
                toggleLoadingSpinner();
                response = await $.get(`/predict?product_id=${productId}`);
                if (!response) {

                    $(".warningNone").text("Количество дней с продажами меньше 50").css("display", "inline");
                    setTimeout(() => {
                        $(".warningNone").css("display", "none").text("");
                    }, 3000); // Скрываем предупреждение через 3 секунды
                    toggleLoadingSpinner();
                } else {
                    $(".warning").css("display", "inline");
                    isForecastMode = !isForecastMode;
                    $(".forecast-button").text("Аналитика");
                    const forecast = response.forecast;
                    updateChartWithForecast(forecast);
                    toggleLoadingSpinner();
                }

            } else {
                isForecastMode = !isForecastMode;
                $(".forecast-button").text("Спрогнозировать");
                const salesResponse = await getMonthlySalesData(productId, months);
                const buysResponse = await getMonthlyBuysData(productId, months);
                createHistogram(salesResponse, buysResponse);
                $(".warning").css("display", "none");
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {

             // Скрываем иконку загрузки после получения ответа
        }
    }

    $(".forecast-button").on("click", async function() {
        await fetchDataAndUpdateChart();
    });

})(jQuery);
