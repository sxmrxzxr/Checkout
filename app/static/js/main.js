$(document).ready(function() {
    $('#inventory').DataTable({
        "scrollY": "650px",
        "scrollCollapse": true,
        "paging": false,
        "autoWidth": false,
        "columns": [
            { "width": "40%"},
            { "width": "20%"},
            { "width": "40%"}
          ]
    });
} );