(async function($){
    "use strict";

    $(".usersHead").addClass("selected");
    let currentRow = null;


    // Функция для заполнения строк таблицы
    async function fillTable(data) {
        const tableBody = $('.tablebody');
        tableBody.empty();

        for (let i = 0; i < data.length; i++) {
            const user = data[i];
            const row = $('<div>').addClass('tablerow').attr('data-id', user.id);

            const numberCell = $('<div>').addClass('tableElem t0').text(i + 1);
            const nameCell = $('<div>').addClass('tableElem t1 employee-name').text(user.name);
            const loginCell = $('<div>').addClass('tableElem t2 employee-login').text(user.login);
            const roleCell = $('<div>').addClass('tableElem t2').text(user.isOwner?"Владелец":"Рабочий");

            // Создание иконок редактирования и удаления
            const actionsCell = $('<div>').addClass('tableElem t2 actions');
            const editIcon = $('<i>').addClass('fa fa-pencil edit-icon');
            const deleteIcon = $('<i>').addClass('fa fa-trash delete-icon');

            // Обработчик события для иконки редактирования работника
            editIcon.on('click', (event) => {
                currentRow = $(event.target).closest('tr'); // Находим строку, которую нужно редактировать
                const employee = {
                    id: row.data('id'), // Предполагается, что ID хранится в атрибуте data-id строки
                    login: row.find('.employee-login').text(), // Предполагается, что логин хранится в элементе с классом employee-login
                    name: row.find('.employee-name').text() // Предполагается, что ФИО хранится в элементе с классом employee-name
                };

                $('#editEmployeeLogin').val(employee.login);
                $('#editEmployeeId').val(employee.id);
                $('#editEmployeeName').val(employee.name);
                $('#editEmployeePassword').val(''); // Оставляем поле пароля пустым

                $('.overlay, .edit-employee-popup').css('display', 'block');
            });

            // Обработчик события для иконки удаления
            deleteIcon.on('click', async () => {
                event.stopPropagation(); // Предотвращаем всплытие события

                if (user.login == $(".login").text().trim()) {
                    // Если пользователь пытается удалить сам себя, выскакивает оповещение
                    const confirmation = confirm('Вы уверены, что хотите удалить свой аккаунт?');

                    if (confirmation) {
                        try {
                            console.log(user.id);
                            const response = await fetch(`/db/users/?user_id=${user.id}`, {
                                method: 'DELETE'
                            });

                            if (response.ok) {
                                row.remove();
                            } else {
                                throw new Error('Ошибка при удалении пользователя');
                            }
                            // Перенаправляем пользователя на страницу авторизации
                            window.location.href = '/auth/formlogin';
                        } catch (error) {
                            console.error('Ошибка при удалении пользователя:', error);
                            alert('Произошла ошибка при удалении пользователя');
                        }
                    }
                } else {
                        // Отправка запроса на сервер для удаления пользователя
                        try {
                            const response = await fetch(`/db/users/?user_id=${user.id}`, {
                                method: 'DELETE'
                            });

                            if (response.ok) {
                                row.remove();
                            } else {
                                throw new Error('Ошибка при удалении пользователя');
                            }

                        } catch (error) {
                            console.error('Ошибка при удалении пользователя:', error);
                            alert('Произошла ошибка при удалении пользователя');
                        }
                    }

            });

            actionsCell.append(editIcon, deleteIcon);
            row.append(numberCell, nameCell, loginCell, roleCell, actionsCell);
            tableBody.append(row);
        }
    }

    async function fetchData(){

    // Отправка запроса на сервер для получения списка складов
        fetch(`/db/users/?skip=0&limit=30&search_query=${$(".search").val()}`)
            .then(function(response) {

                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Ошибка при получении списка складов');
                }
            })
            .then(function(data) {

                fillTable(data);
                console.log(data);
            })
            .catch(function(error) {
                console.error("Ошибка при чтении классов: ", error);
            });
    }

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
    $('#editEmployeeForm').on('submit', async function(event) {
        event.preventDefault();

        const data = {
            id: $('#editEmployeeId').val(),
            login: $('#editEmployeeLogin').val(),
            name: $('#editEmployeeName').val(),
            password: $('#editEmployeePassword').val(),
            idCompany: null,
            email: "",
            is_active: true,
            is_superuser: false,
            is_verified: false
        };


        try {

            // Затем обновляем остальные данные пользователя
            const response = await updateUser(data);

            console.log(response);

            // Обновление данных работника в текущей строке
            if (currentRow) {
                currentRow.find('.employee-login').text(data.login);
                currentRow.find('.employee-name').text(data.name);
            }

            $('.overlay, .edit-employee-popup').css('display', 'none');

        } catch (error) {
            console.error('Ошибка при обновлении пользователя:', error);
            alert('Произошла ошибка при обновлении данных пользователя');
        }
    });

    // Закрытие всплывающего окна при клике на overlay
    $('.overlay').on('click', function() {
        $('.overlay, .edit-popup, .edit-employee-popup').css('display', 'none');
    });

    async function updateUser(data) {
        const response = await fetch('/db/users/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    }

    await fetchData();

})(jQuery);