
CategoryTree = function (params) {

    var $container = params.$container,
        $filter = params.$filter,
        $input = params.$input,
        data = params.data;

    function handleFilterKeyup() {
        var val = $(this).val();

        if (!val) {
            $container.treeview('clearSearch');
            return;
        }

        $container.treeview('search', [val, {
            ignoreCase: true,
            exactMatch: false,
            revealResults: true
        }]);
    }

    function handleSearchComplete() {
        var $c = $container,
            tree = $c.treeview(true);

        $.each(tree.getEnabled(), function () {
            var $li = $c.find('[data-nodeid=' + this.nodeId + ']');
            $li[this.searchResult ? 'show' : 'hide']();
        })
    }

    function handleSearchCleared() {
        $container.find('li').show();
    }

    function handleNodeSelected(event, node) {
        $input.val(node.id).trigger('change');
    }

    function handleNodeUnselected(event, node) {
        $input.val('').trigger('change');
    }

    $container.treeview({
        data: data,
        nodeIcon: 'fa fa-folder',
        highlightSearchResults: false,
        onSearchComplete: handleSearchComplete,
        onSearchCleared: handleSearchCleared,
        onNodeSelected: handleNodeSelected,
        onNodeUnselected: handleNodeUnselected
    });

    $filter.on('keyup', handleFilterKeyup);

};
