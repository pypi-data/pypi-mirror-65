
SelectProductList = function (params) {

    var $container = params.$container;

    function handleListItemDoubleClick() {
        $(window).trigger('product-selected', [$(this).data('item-id')]);
    }

    function handleItemUpdated(event, item) {
        getItemContainer(item.id)
            .find('[data-role=stock]')
            .text(item.stock);
    }

    function getItemContainer(itemId) {
        return $container.find(
            '[data-role=list-item][data-item-id=' + itemId + ']');
    }

    $container.on('dblclick', '[data-role=list-item]', handleListItemDoubleClick);

    $(window).on('product-updated', handleItemUpdated);

};
