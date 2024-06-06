(async function($){
    "use strict";

    var input=$('.validate-input .input100');

    $('.register100-form').submit(async function(event) {

        event.preventDefault(); // Предотвращаем обычное поведение формы


        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check){

            const username = $('[name="username"]').val();
            const name = $('[name="name"]').val();
            const password = $('[name="pass"]').val();
            const dublepass = $('[name="dublepass"]').val();

            const response = await fetch(`http:/\/127.0.0.1:8000/auth/check-login?login=${username}`);
            const data = await response.json();
            console.log(data);

            if(data.exists){
                check = false;
                showValidate2($('[name="username"]'));
            }

            if (password != dublepass) {
                showValidate2($('[name="dublepass"]'));
                check = false;
            }

            if (check){
                const data = {
                    'login': username,
                    'password': password,
                    'email': null,
                    'idCompany': null,
                    'name': name,
                    'isOwner': true
                };

                $.ajax({
                url: '/auth/register',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    const data = {
                        'username': username,
                        'password': password
                    };
                    $.ajax({
                        url: '/auth/login',
                        type: 'POST',
                        contentType: 'application/x-www-form-urlencoded',
                        data: data,
                        success: function(response) {
                            window.location.href = '/company/addCompany';
                        },
                        error: function(xhr, status, error) {
                            console.error('Ошибка при входе:', status, error);
                        }
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при регистрации:', status, error);
                    console.log(data);
                }
            });

            }

        }
    });


    $('.register100-form-worker').submit(async function(event) {

        event.preventDefault(); // Предотвращаем обычное поведение формы


        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check){

            const username = $('[name="worker_log"]').val();
            const name = $('[name="FIO"]').val();
            const password = $('[name="work_pas"]').val();
            const isOwner = $('[name="isOwner"]').is(':checked');


            const response = await fetch(`http:/\/127.0.0.1:8000/auth/check-login?login=${username}`);
            const data = await response.json();
            console.log(data);

            if(data.exists){
                check = false;
                showValidate2($('[name="worker_log"]'));
            }

            if (check){
                const data = {
                    'login': username,
                    'password': password,
                    'email': null,
                    'idCompany': null,
                    'name': name,
                    'isOwner': isOwner
                };

                $.ajax({
                url: '/db/users',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    window.location.href = '/company/users';
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при регистрации:', status, error);
                    console.log(data);
                }
            });

            }

        }
    });








    $('.register100-form-company').submit(async function(event) {

        event.preventDefault(); // Предотвращаем обычное поведение формы


        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check){

            const name = $('[name="namecompany"]').val();
            const email = $('[name="email"]').val();
            const address = $('[name="address"]').val();
            const type = $('[name="type"]').val();

            const data = {
                'name': name,
                'email': email,
                'address': address,
                'type': type
            };

            $.ajax({
            url: '/db/company',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                window.location.href = '/company/company';
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при создании компании:', status, error);
                console.log(data);
            }
        });

        }
    });

    $('.login100-form').submit(function(event) {
        event.preventDefault();


        var check=true;
        for(var i=0;i<input.length;i++){
            if(validate(input[i])==false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check){
            // Считываем значения полей формы
            const username = $('[name="username"]').val();
            const password = $('[name="password"]').val();


            // Создаем объект с данными для отправки
            const data = {
                'username': username,
                'password': password
            };

            // Отправляем POST-запрос на сервер
            $.ajax({
                url: '/auth/login',
                type: 'POST',
                contentType: 'application/x-www-form-urlencoded',
                data: data,
                success: function(response) {
                    window.location.href = '/company/company';
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при входе:', status, error);
                    showValidate3($('[class="not-match"]'));
                }
            });
        }
    });

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
            hideValidate(this);
            hideValidate2(this);
            $('[class="not-match"]').css("display", "none")
        });
    });

    function validate(input){
        if($(input).val().trim()==''){
            return false;
        }
    }

    function showValidate2(input){
        var thisAlert=$(input).parent().parent();
        $(thisAlert).addClass('alert-validate');}

    function showValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).addClass('alert-validate');}

    function hideValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }
    function hideValidate2(input){
        var thisAlert=$(input).parent().parent();
        $(thisAlert).removeClass('alert-validate');
    }
    function showValidate3(input){
        var thisAlert=$(input);
        $(thisAlert).css("display", "inline")
    }
//    function hideValidate3(input){
//        var thisAlert=$(input);
//        $(thisAlert).css("display", "none")
//    }
})(jQuery);