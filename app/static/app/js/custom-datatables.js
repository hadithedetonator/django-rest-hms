(function ($) {
    "use strict"; // Start of use strict
    /* ====================
    Data tables
    =======================*/
    
    $('#tableId').DataTable({
        "order": [],
        "columnDefs": [{
            "targets": 'no-sort',
            "orderable": false,
        }]
    });
    
})(jQuery);
