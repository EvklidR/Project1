(async function($){
    "use strict"

    $('.login100-form-store').submit(function(event) {
        event.preventDefault();

        const address = $('[name="address"]').val();
        const type = $('[name="type"]').val();

        if (address.trim() == ""){
            showValidate($('[name="address"]'));
        } else{

            const data = {
                'name': address,
                "type": type,
                "idCompany": null
            };

            console.log(data);

            fetch('/db/stores', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    window.location.href = '/company/stores';
                })
                .catch(error => {
                    console.error('Ошибка при добавлении товара:', error);
                });
        }
    });

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
            hideValidate(this);
            $('[class="not-match"]').css("display", "none");
        });
    });

    function showValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input){
        var thisAlert=$(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }

})(jQuery);