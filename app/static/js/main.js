$(document).ready(function() {
    $('#inventory').DataTable({
        "paging": false,
        "autoWidth": false,
        "scrollY": "75%",
        "scrollCollapse": true,
        "columns": [
            { "width": "20%"},
            { "width": "5%"},
            { "width": "15%"},
            { "width": "20%"},
            { "width": "20%"},
            { "width": "20%"}
          ],
        "order": [[ 1, "desc" ], [ 0, "asc" ]]
    });
} );

$(document).ready(function() {
    $('#hackathons').DataTable({
        "paging": false,
        "autoWidth": false,
        "columns": [
            { "width": "40%"},
            { "width": "20%"},
            { "width": "40%"}
          ],
        "order": [[ 2, "desc" ]],
        "scrollY": "150px",
        "scrollCollapse": true,
        bFilter: false,
        bInfo: false
    });
} );