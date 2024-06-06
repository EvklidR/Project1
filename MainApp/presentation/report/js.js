$(document).ready(async function() {

    let revenueChart; // Переменная для хранения объекта графика

    var currentDate = new Date().toLocaleDateString();
    $("#current-date").text("Текущая дата: " + currentDate);

    function getCompanyData(period) {
        return $.get(`/db/get_company_data?period=${period}`);
    }

    function getMonthlyRevenue(period) {
        return $.get(`/db/getMonthlyRevenue?period=${period}`);
    }

    function createRevenueChart(data) {
        const labels = Object.keys(data);
        const revenueValues = Object.values(data);

        if (revenueChart) {
            revenueChart.destroy(); // Уничтожаем предыдущий график перед созданием нового
        }

        const ctx = document.getElementById('revenueChart').getContext('2d');
        revenueChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Выручка',
                    data: revenueValues,
                    backgroundColor: 'rgba(255, 165, 0, 0.2)', // Оранжевый цвет столбцов
                    borderColor: 'rgba(255, 165, 0, 1)', // Оранжевый цвет границ столбцов
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Месяцы',
                            color: '#000'
                        },
                        ticks: {
                            color: '#000' // Черный цвет меток на оси X
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Выручка',
                            color: '#000'
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

    async function getData(period) {
        try {
            const companyResponse = await fetch("/db/get_company");
            const company = await companyResponse.json();
            console.log(company);
            $(".title").text(company.name);

            const companyDataResponse = await getCompanyData(period);
            const companyData = companyDataResponse;
            // Обработка полученных данных
            $("#totalRevenue").text(companyData.totalRevenue);
            $("#totalSales").text(companyData.totalSales);
            $("#totalBuys").text(companyData.totalBuys);
            $("#totalReturns").text(companyData.totalReturns);
            $("#totalProducts").text(companyData.totalProducts);
            $("#totalStores").text(companyData.totalStores);
            $("#totalEmployees").text(companyData.totalEmployees);

            const monthlyRevenueDataResponse = await getMonthlyRevenue(period);
            const monthlyRevenueData = monthlyRevenueDataResponse;
            createRevenueChart(monthlyRevenueData);
        } catch (error) {
            console.error("Error fetching company data:", error);
        }
    }

    $('#months').on('change', async function() {
        const initialPeriod = $('#months').val();
        await getData(initialPeriod);
    });

    const initialPeriod = $('#months').val();
    await getData(initialPeriod);

    $("#downloadPdfButton").on("click", async function() {
        try {
                      // Получение заголовка и текущей даты
            const titleText = $(".title").text();
            const currentDate = new Date().toLocaleDateString();
            const period = $("#months").val();
            const periodText = "Данные взяты за " + period + " месяца"
            console.log(periodText);

            // Создание canvas для заголовка и даты
            const titleCanvas = document.createElement('canvas');
            const titleContext = titleCanvas.getContext('2d');
            titleCanvas.width = 800;
            titleCanvas.height = 50;
            titleContext.fillStyle = '#ffffff'; // Белый цвет фона
            titleContext.fillRect(0, 0, titleCanvas.width, titleCanvas.height);
            titleContext.fillStyle = '#000000'; // Черный цвет текста
            titleContext.font = '20px Arial';
            titleContext.fillText(titleText, 10, 20);
            titleContext.font = '16px Arial';
            titleContext.fillText(currentDate, 10, 40);
            titleContext.fillText(periodText, 100, 40);

            // Преобразование элементов в изображения с помощью html2canvas
            const chartCanvas = await html2canvas(document.querySelector("#revenueChart"), {
                windowWidth: document.querySelector("#revenueChart").scrollWidth,
                windowHeight: document.querySelector("#revenueChart").scrollHeight,
                scale: 2,
                useCORS: true,
                background: "#ffffff"
            });

            const tableCanvas = await html2canvas(document.querySelector("#companyInfo"), {
                windowWidth: document.querySelector("#companyInfo").scrollWidth,
                windowHeight: document.querySelector("#companyInfo").scrollHeight,
                scale: 2,
                useCORS: true,
                background: "#ffffff"
            });

            // Получение размеров элементов
            const titleWidth = titleCanvas.width;
            const titleHeight = titleCanvas.height;
            const chartWidth = chartCanvas.width;
            const chartHeight = chartCanvas.height;
            const tableWidth = tableCanvas.width;
            const tableHeight = tableCanvas.height;

            // Преобразование canvas в data-URL изображения
            const titleImgData = titleCanvas.toDataURL('image/jpeg', 0.95);
            const chartImgData = chartCanvas.toDataURL('image/jpeg', 0.95);
            const tableImgData = tableCanvas.toDataURL('image/jpeg', 0.95);

            // Создание PDF-документа с помощью jsPDF
            const pdf = new jsPDF({
                orientation: 'landscape',
                unit: 'px',
                format: [Math.max(titleWidth, chartWidth, tableWidth) + 40, titleHeight + chartHeight + 60]
            });

            // Добавление изображений в PDF-документ
            pdf.addImage(titleImgData, 'JPEG', 20, 30, titleWidth, titleHeight);
            pdf.addImage(chartImgData, 'JPEG', 20, 120 + titleHeight, chartWidth - 180, chartHeight - 180);
            pdf.addImage(tableImgData, 'JPEG', 20 + chartWidth - 170, 120 + titleHeight, tableWidth - 210, tableHeight - 100);

            // Сохранение PDF-файла
            pdf.save('report.pdf');
        } catch (error) {
            console.error("Error generating PDF:", error);
        }
    });

});
