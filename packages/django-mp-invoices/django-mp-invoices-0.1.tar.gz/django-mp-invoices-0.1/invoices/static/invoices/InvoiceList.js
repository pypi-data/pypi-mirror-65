
InvoiceList = function (params) {

    var $container = params.$container,
        addItemUrl = params.addItemUrl;

    function handleListItemSelected(event, itemId) {
        $.ajax({
            url: addItemUrl,
            method: 'POST',
            data: {'product_id': itemId},
            success: handleAddItemSuccess,
            error: handleAddItemError
        });
    }

    function handleAddItemSuccess(response) {
        var $items = getItemsContainer(),
            $item = getItemContainer(response.item_id);

        if ($item.length) {
            $item.replaceWith(response.html);
        } else {
            $items.prepend(response.html);
        }

        $(window).trigger('product-updated', response.product);
    }

    function handleAddItemError(response) {
        $.notify({message: response.responseText}, {type: 'danger'});
    }

    function getItemsContainer() {
        return $container.find('[data-role=list-items]');
    }

    function getItemContainer(itemId) {
        return getItemsContainer().find(
            '[data-role=list-item][data-item-id=' + itemId + ']');
    }

    new CellInput({
        $container: $container,
        selector: '[data-role=qty-input]'
    });

    new DeleteAction({
        $container: $container,
        selector: '[data-role=delete-action]',
        onDelete: function (itemId) {
            getItemContainer(itemId).remove();
        }
    });

    $(window).on('product-selected', handleListItemSelected);

};
