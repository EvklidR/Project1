(function($){
    "use strict";

    $.ajax({
        url: '/auth/logout',
        type: 'POST',
        success: function(response) {
            console.log("logout successfully");
        },
        error: function(xhr, status, error) {
            console.error('Ошибка при выходе:', status, error);
        }
    });
})(jQuery);