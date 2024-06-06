(async function($){
    "use strict"

    const overlay = $('.overlay');
    const popup = $('.popup');
    const selectButton = $('.select-button');
    const chooseButton = $('.choose-button');
    const groupList = $('.popup ul');
    const addIcon = $('.add-icon');
    const groupInput = $('.group-input');
    const sel = $(".sel");

    let lastEditedItem = null;

    $('.login100-form-product').submit(function(event) {
        event.preventDefault();

        var input=$('.validate-input .input100');

        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check) {
            const  prodName = $('[name="nameprod"]').val();
            var expiry = $('[name="expiry"]').val();
            const group = $('[name="group"]').val();
            const unit = $('[name="unit"]').val();
            const period = $('[name="period"]').val();

            if (period == "2") {
                expiry = Number(expiry)*30;
            } else if (period == "3") {
                expiry = Number(expiry)*360;
            }

            const data = {
                'name': prodName,
                "data_licvid": expiry,
                "type": group,
                "unit": unit,
                "idCompany": null
            };

            console.log(data);

            fetch('/db/product', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    window.location.href = '/company/company';
                })
                .catch(error => {
                    console.error('Ошибка при добавлении товара:', error);
                });
        }
    });

    // Обработчик события для кнопки "Выбрать"
    selectButton.on('click', function() {
        hideValidate($('[name="group"]'));
        $(".alert").css("display", "none");
        groupInput.val("");

        // Отправка запроса на сервер для получения списка групп
        fetch('/db/group')
            .then(response => response.json())
            .then(data => {
                // Очистка списка групп
                groupList.empty();

                // Заполнение списка названиями групп и иконками редактирования и корзины
                data.forEach(group => {
                    const listItem = $('<li>');
                    const groupName = $('<span>').addClass('group-name').text(group.name);
                    const iconWrapper = $('<div>').addClass('icon-wrapper');
                    const editIcon = $('<span>').addClass('edit-icon').html('&#9998;'); // Иконка редактирования
                    const deleteIcon = $('<span>').addClass('delete-icon').html('&#128465;'); // Иконка удаления
                    iconWrapper.append(editIcon, deleteIcon);

                    listItem.append(groupName, iconWrapper);
                    groupList.append(listItem);
                });

                // Показываем overlay и всплывающее окно
                overlay.css('display', 'block');
                popup.css('display', 'block');
            })
            .catch(error => {
                console.error('Ошибка при получении списка групп:', error);
            });
    });

    // Обработчик события для выбора пункта из меню в блоке popup
    groupList.on('click', 'li', function() {
        const listItem = $(this);

        // Если есть предыдущий редактируемый элемент, завершаем его редактирование
        if (lastEditedItem && lastEditedItem[0] !== listItem[0]) {
            finishEditing(lastEditedItem);
        }

        // Удаляем класс "selected" у всех элементов списка
        groupList.find('li').removeClass('selected');
        // Добавляем класс "selected" к выбранному элементу списка
        listItem.addClass('selected');

        // Деактивируем кнопку "Выбрать", если выбранный элемент находится в режиме редактирования
        if (listItem.hasClass('editing')) {
            chooseButton.addClass("disabled");
        } else {
            chooseButton.removeClass("disabled");
        }
    });

    // Обработчик события для кнопки "Выбрать"
    chooseButton.on('click', function() {
        // Получаем выбранный элемент списка
        const selectedValue = groupList.find('li.selected .group-name').text().trim();

        // Подставляем выбранное значение в поле "group"
        $('input[name="group"]').val(selectedValue);

        // Скрываем overlay и всплывающее окно
        overlay.css('display', 'none');
        popup.css('display', 'none');

        // Сбрасываем выбранный элемент и деактивируем кнопку "Выбрать"
        chooseButton.addClass("disabled");
    });

    // Функция для завершения редактирования
    function finishEditing(listItem) {
        const editInput = listItem.find('.edit-input');
        const oldGroupName = listItem.attr('data-old-name');

        // Проверяем, есть ли обертка с сообщением об ошибке
        const wrapperError = listItem.find('.wrapper-error');
        if (wrapperError.length) {
            // Вытаскиваем editInput из обертки
            editInput.detach();
            // Удаляем обертку с сообщением об ошибке
            wrapperError.remove();
            // Вставляем editInput обратно в listItem перед иконками
            listItem.prepend(editInput);
        }

        // Восстанавливаем исходное состояние элемента
        editInput.replaceWith($('<span class="group-name">').text(oldGroupName));
        listItem.find('.save-icon').replaceWith($('<span class="edit-icon">&#9998;</span>'));
        listItem.removeClass('editing').removeClass('selected');
        listItem.removeAttr('data-old-name');
    }


    // Обработчик события для иконки редактирования
    groupList.on('click', '.edit-icon', function(event) {
        event.stopPropagation();
        const listItem = $(this).closest('li');
        const groupNameSpan = listItem.find('.group-name');
        const groupName = groupNameSpan.text().trim();

        // Если есть предыдущий редактируемый элемент, завершаем его редактирование
        if (lastEditedItem && lastEditedItem[0] !== listItem[0]) {
            finishEditing(lastEditedItem);
        }

        // Сохраняем текущий элемент как последний редактируемый
        lastEditedItem = listItem;

        // Сохраняем первоначальное название в атрибуте data-old-name
        listItem.attr('data-old-name', groupName);

        const editInput = $('<input type="text" class="edit-input">').val(groupName);
        groupNameSpan.replaceWith(editInput);
        const saveIcon = $('<span class="save-icon">&#10004;</span>');
        $(this).replaceWith(saveIcon);

        listItem.addClass('editing');

        // Удаляем класс "selected" у всех элементов списка
        groupList.find('li').removeClass('selected');
        // Добавляем класс "selected" к текущему элементу
        listItem.addClass('selected');


        // Добавляем обработчик для изменения текста в поле ввода
        editInput.on('input', function() {
            const newValue = $(this).val().trim();
            const oldValue = listItem.attr('data-old-name');
            if (!newValue) {
                saveIcon.addClass('disabled');
            } else {
                saveIcon.removeClass('disabled');
            }
        });

        // Деактивируем кнопку "Выбрать" при редактировании
        chooseButton.addClass("disabled");
    });

    // Обработчик события для иконки сохранения
    groupList.on('click', '.save-icon', async function(event) {
        event.stopPropagation();
        const listItem = $(this).closest('li');
        const editInput = listItem.find('.edit-input');
        const newGroupName = editInput.val().trim();
        const oldGroupName = listItem.attr('data-old-name');

        if (newGroupName && newGroupName !== oldGroupName) {
            // Проверяем, существует ли новое название группы в компании
            const responseCheckGroup = await fetch(`/db/get_group_id?group_name=${newGroupName}`);
            const groupExists = await responseCheckGroup.json();

            if (!groupExists) {

                const Group = await fetch(`/db/get_group_id?group_name=${oldGroupName}`);
                const group = await Group.json();

                const data = {
                    name: newGroupName,
                    id: group["id"],
                    idCompany: null
                };

                try {
                    // Отправка запроса на сервер для обновления группы
                    const response = await fetch('/db/group', {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
                    const responseData = await response.json();
                    console.log(responseData);

                    editInput.replaceWith($('<span class="group-name">').text(newGroupName));
                    $(this).replaceWith($('<span class="edit-icon">&#9998;</span>'));

                    // Проверяем, есть ли обертка с сообщением об ошибке
                    const wrapperError = listItem.find('.wrapper-error');
                    if (wrapperError.length) {
                        // Вытаскиваем editInput из обертки
                        editInput.detach();
                        // Удаляем обертку с сообщением об ошибке
                        wrapperError.remove();
                        // Вставляем editInput обратно в listItem перед иконками
                        listItem.prepend(editInput);
                    }

                } catch (error) {
                    console.error('Ошибка при обновлении группы:', error);
                }

                chooseButton.removeClass('disabled');
                listItem.removeClass('editing');

            } else {
                // Если группа уже существует, создаем обертку для ошибки и поля для ввода
                const errorMessage = $('<span class="error-message">').text('Такая группа уже существует');
                const wrapperError = $('<div class="wrapper-error">').append(errorMessage, editInput);
                listItem.prepend(wrapperError);
            }
        } else {
            editInput.replaceWith($('<span class="group-name">').text(oldGroupName));
            $(this).replaceWith($('<span class="edit-icon">&#9998;</span>'));
            chooseButton.removeClass('disabled');
            listItem.removeClass('editing');
        }

    });


    // Обработчик события для overlay
    overlay.on('click', function() {
        if (lastEditedItem) {
            finishEditing(lastEditedItem);
            lastEditedItem = null;
        }

        // Скрываем overlay и всплывающее окно
        chooseButton.addClass('disabled');
        overlay.css('display', 'none');
        popup.css('display', 'none');
    });


    // Обработчик события для иконки удаления
    groupList.on('click', '.delete-icon', function(event) {
        event.stopPropagation(); // Предотвращаем всплытие события

        const listItem = $(this).closest('li');
        const group = listItem.find('.group-name').text().trim();

        // Отправка запроса на сервер для удаления элемента из базы данных
        fetch(`/db/group/?group_name=${group}`, {
            method: 'DELETE'
        })
            .then(response => {
                // Удаление элемента из списка
                listItem.remove();
            })
            .catch(error => {
                console.error('Ошибка при удалении элемента:', error);
            });
    });

    // Обработчик события для поля ввода группы
    groupInput.on('input', function() {
        const inputValue = $(this).val().trim();
        $(".alert").css("display", "none");

        // Проверяем, является ли введенное значение пустым
        if (inputValue === '') {
            // Деактивируем кнопку "Сохранить"
            addIcon.addClass('disabled');
        } else {
            // Активируем кнопку "Сохранить"
            addIcon.removeClass('disabled');
        }
    });

    // Обработчик события для кнопки "Сохранить"
    addIcon.on('click', function() {
        var inputValue = groupInput.val().trim();

        // Проверяем, является ли введенное значение пустым
        if (inputValue === '') {
            return;
        }

        for (let name in groupList.find("li .group-name")) {
            if (inputValue == groupList.find("li .group-name")[name].innerHTML) {
                $(".alert").css("display", "block");
                return;
            }
        }

        // Отправка запроса на сервер для сохранения значения в базу данных
        fetch('/db/group', {
            method: 'POST',
            body: JSON.stringify(
                {
                    "name": inputValue,
                    "idCompany": null,
                }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                // Отправка запроса на сервер для получения списка групп
                fetch('/db/group')
                    .then(response => response.json())
                    .then(data => {
                        // Очистка списка групп
                        groupList.empty();

                        // Заполнение списка названиями групп и иконками редактирования и корзины
                        data.forEach(group => {
                            const listItem = $('<li>');
                            const groupName = $('<span>').addClass('group-name').text(group.name);
                            const iconWrapper = $('<div>').addClass('icon-wrapper');
                            const editIcon = $('<span>').addClass('edit-icon').html('&#9998;'); // Иконка редактирования
                            const deleteIcon = $('<span>').addClass('delete-icon').html('&#128465;'); // Иконка удаления
                            iconWrapper.append(editIcon, deleteIcon);

                            listItem.append(groupName, iconWrapper);
                            groupList.append(listItem);
                        });

                        // Показываем overlay и всплывающее окно
                        overlay.css('display', 'block');
                        popup.css('display', 'block');
                    })
                    .catch(error => {
                        console.error('Ошибка при получении списка групп:', error);
                    });
            })
            .catch(error => {
                console.error('Ошибка при сохранении значения:', error);
            });
        groupInput.val('');
        addIcon.addClass('disabled');
    });

    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
            $('[class="not-match"]').css("display", "none");
        });
    });

    function validate(input) {
        if ($(input).val().trim() == '') {
            return false;
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }

})(jQuery);
