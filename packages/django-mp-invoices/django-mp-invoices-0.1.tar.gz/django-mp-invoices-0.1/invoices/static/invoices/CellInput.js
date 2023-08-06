
CellInput = function (params) {

    var $container = params.$container,
        selector = params.selector;

    function handleInputChange() {
        var $input = $(this);

        $input.blur();

        $.post($input.data('url'), {value: $input.val()})
            .done(handleSaveSuccess)
            .error(handleSaveError);
    }

    function handleSaveSuccess(response) {
        $(window).trigger('product-updated', response.product);
        $.notify({message: response.message}, {type: 'success'});
    }

    function handleSaveError(response) {
        $.notify({message: response.responseText}, {type: 'danger'});
    }

    function handleInputFocus() {
        $(this).select();
    }

    $container.on('change', selector, handleInputChange);
    $container.on('focus', selector, handleInputFocus);

};
