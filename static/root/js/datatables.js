// All worlds table

$(document).ready(function () {
    $('#worlds_table').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "emptyTable": ""
        },

        // sortowanie po pierwszym wczytaniu
        order: [[0, 'asc']],

        // szerokość automatyczna
        "autoWidth": false,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": false,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [10, 25, 500, -1],
            [10, 25, 500, 'All'],
        ],

        // opcje do paginacji
        //"pageLength": 10,
        "paging": false,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [ 1, 2, 3, 4 ] }],
        "dom": "<'row float-start'<'col-md'f>>"
    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');

} );


// single world online list
$(document).ready(function () {
    $('#single-world-table').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: { search: "", searchPlaceholder: "Search...",
         lengthMenu: "_MENU_"},

        // sortowanie po pierwszym wczytaniu
        order: [[0, 'asc']],

        // szerokość automatyczna
        "autoWidth": false,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": false,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [10, 25, 500, -1],
            [10, 25, 500, 'All'],
        ],

        // opcje do paginacji
        //"pageLength": 10,
        "paging": false,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [ 0, 1, 2 ] }],
        "dom": "<'row float-start'<'col-md'f>>"
    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');

} );


// test
$(document).ready(function () {
    $('#test_table2').DataTable( {
        "searching": true,
        language: { search: "", searchPlaceholder: "Search...",
         lengthMenu: "_MENU_"},
        order: [[4, 'desc']],
        "autoWidth": false,
        "ordering": true,
        "responsive": false,
        "bLengthChange": false,
        lengthMenu: [
            [10, 25, 500, -1],
            [10, 25, 500, 'All'],
        ],
        //"pageLength": 10,
        "paging": false,
        "pagingType": 'full_numbers',
        "bInfo": false,


        "aoColumnDefs": [
        { "bSearchable": false, "aTargets": [ 1, 2, 3, 4 ] }],
        "dom": "<'row float-start'<'col-md'f>>"
    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');

} );

// top500
$(document).ready(function () {
    $('#top-500').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "emptyTable": ""
        },

        // sortowanie po pierwszym wczytaniu
        order: [[5, 'desc']],

        // szerokość automatyczna
        "autoWidth": false,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": false,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [10, 25, 500, -1],
            [10, 25, 500, 'All'],
        ],

        // opcje do paginacji
        //"pageLength": 10,
        "paging": false,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4, 5, 6, 7, 8 ] }],
        "dom": "<'row float-start'<'col-md'f>>"
    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');

} );

// mainland
$(document).ready(function () {
    $('#mainland').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "zeroRecords": "Select world"
        },

        // sortowanie po pierwszym wczytaniu
        order: [[7, 'desc']],

        // szerokość automatyczna
        "autoWidth": true,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": true,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [25, 50, 100, 250, 500, -1],
            [25, 50, 100, 250, 500, 'All'],
        ],

        // opcje do paginacji
        "pageLength": 100,
        "paging": true,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4, 5, 6, 7 ] }],
        // "dom": "<'row float-start'<'col-md'f>>"

        // pozycjonowanie
        "dom": "<'row d-flex justify-content-between'<'col-sm-3'f><'col-sm-3'<'row'<'col-sm-1'><'col-sm-1'l>>>><'row'<'col-md-12't>><'row'<'col-sm-12'p>>"



    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');
    // $('.dataTables_paginate .paginate_button:active').addClass('btn btn-outline-link m-2');

} );


// rookgaard
$(document).ready(function () {
    $('#rookgaard').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "zeroRecords": "Select world"
        },

        // sortowanie po pierwszym wczytaniu
        order: [[5, 'desc']],

        // szerokość automatyczna
        "autoWidth": true,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": false,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [25, 50, 100, 250, 500, -1],
            [25, 50, 100, 250, 500, 'All'],
        ],

        // opcje do paginacji
        "pageLength": 100,
        "paging": false,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4, 5, 6, 7, 8 ] }],
        "dom": "<'row float-start'<'col-md'f>>"

        // pozycjonowanie
        //"dom": "<'row d-flex justify-content-between'<'col-sm-3'f><'col-sm-3'<'row'<'col-sm-1'><'col-sm-1'l>>>><'row'<'col-md-12't>><'row'<'col-sm-12'p>>"



    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');
    // $('.dataTables_paginate .paginate_button:active').addClass('btn btn-outline-link m-2');

} );


// explore
$(document).ready(function () {
    $('#explore').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "zeroRecords": "Chose you filters"
        },

        // sortowanie po pierwszym wczytaniu
        order: [[3, 'desc']],

        // szerokość automatyczna
        "autoWidth": true,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": true,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [25, 50, 100, 250, 500, 1000, -1],
            [25, 50, 100, 250, 500, 1000, 'All'],
        ],

        // opcje do paginacji
        "pageLength": 100,
        "paging": true,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4, 5, 6, 7, 8 ] }],
        //"dom": "<'row float-start'<'col-md'f>>"

        // pozycjonowanie
        "dom": "<'row d-flex justify-content-between'<'col-sm-3'f><'col-sm-3'<'row'<'col-sm-1'><'col-sm-1'l>>>><'row'<'col-md-12't>><'row'<'col-sm-12'p>>"



    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');
    // $('.dataTables_paginate .paginate_button:active').addClass('btn btn-outline-link m-2');

} );


// transfers
$(document).ready(function () {
    $('#transfers_table').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "zeroRecords": "Chose you filters"
        },

        // sortowanie po pierwszym wczytaniu
        // order: [[3, 'desc']],

        // szerokość automatyczna
        "autoWidth": true,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": true,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [25, 50, 100, 250, 500, 1000, -1],
            [25, 50, 100, 250, 500, 1000, 'All'],
        ],

        // opcje do paginacji
        "pageLength": 100,
        "paging": true,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4, 5, 6 ] }],
        //"dom": "<'row float-start'<'col-md'f>>"

        // pozycjonowanie
        "dom": "<'row d-flex justify-content-between'<'col-sm-3'f><'col-sm-3'<'row'<'col-sm-1'><'col-sm-1'l>>>><'row'<'col-md-12't>><'row'<'col-sm-12'p>>"



    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');
    // $('.dataTables_paginate .paginate_button:active').addClass('btn btn-outline-link m-2');

} );


// name_change_table
$(document).ready(function () {
    $('#name_change_table').DataTable( {
        // czy mozna szukac
        "searching": true,

        // pole do szukania
        language: {
                    search: "",
                    searchPlaceholder: "Search...",
                    lengthMenu: "_MENU_",
                    "zeroRecords": "Chose you filters"
        },

        // sortowanie po pierwszym wczytaniu
        // order: [[3, 'desc']],

        // szerokość automatyczna
        "autoWidth": true,

        // możliwość sortowania
        "ordering": true,

        "responsive": true,
        "bLengthChange": true,

        // ustawienia do wyswietlania danej liczby wynikow
        lengthMenu: [
            [25, 50, 100, 250, 500, 1000, -1],
            [25, 50, 100, 250, 500, 1000, 'All'],
        ],

        // opcje do paginacji
        "pageLength": 100,
        "paging": true,
        "pagingType": 'full_numbers',

        // nie pamiętam
        "bInfo": false,

        // search engine
        "aoColumnDefs": [
        { "bSearchable": true, "aTargets": [0, 1, 2, 3, 4 ] }],
        //"dom": "<'row float-start'<'col-md'f>>"

        // pozycjonowanie
        "dom": "<'row d-flex justify-content-between'<'col-sm-3'f><'col-sm-3'<'row'<'col-sm-1'><'col-sm-1'l>>>><'row'<'col-md-12't>><'row'<'col-sm-12'p>>"



    }
    );
    $('div.dataTables_filter input').addClass('form-control bg-dark border-0');
    $('div.dataTables_length select').addClass('form-select form-select-sm mb-3');
    // $('.dataTables_paginate .paginate_button:active').addClass('btn btn-outline-link m-2');

} );