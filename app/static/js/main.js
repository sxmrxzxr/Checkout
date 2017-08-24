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
    $('#inventory_admin').DataTable({
        "paging": false,
        "autoWidth": false,
        "scrollY": "75%",
        "scrollCollapse": true,
        "columns": [
            { "width": "10%"},
            { "width": "25%"},
            { "width": "5%"},
            { "width": "20%"},
            { "width": "20%"},
            { "width": "20%"}
          ],
        "order": [[ 1, "desc" ], [ 0, "asc" ]]
    });
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
    $(document).on('submit','#add_hackathon', function(event) {
        $.ajax({
            data : {
                'name': $('#hackathon_name').val(),
                'location': $('#location').val(),
                'date': $('#date_range').val(),
                'link': $('#link').val()
            },
            type : 'POST',
            url : '/add_hackathon'
        }).done(function(data) {
            location.reload();
        });
        event.preventDefault();
    });
    $(document).on('submit','#remove_hackathon', function(event) {
        $.ajax({
            data : {
                'name': $('#r_hackathon_name').val()
            },
            type : 'POST',
            url : '/remove_hackathon'
        }).done(function(data) {
            location.reload();
        });
        event.preventDefault();
    });
    $(document).on('submit','#add_item', function(event) {
        $.ajax({
            data : {
                'name': $('#item_name').val(),
                'quantity': $('#add_item_quant').val(),
                'res_length': $('#res_length').val(),
                'category': $('#item_category').val(),
                'item_link': $('#item_link').val(),
                'item_id': $('#item_id').val()
            },
            type : 'POST',
            url : '/add_item'
        }).done(function(data) {
            location.reload();
        });
        event.preventDefault();
    });
    $(document).on('submit','#increase_quantity', function(event) {
        $.ajax({
            data : {
                'item_id': $('#increase_item_id').val(),
                'quantity': $('#increase_item_quantity').val()
            },
            type : 'POST',
            url : '/increase_quantity'
        }).done(function(data) {
            location.reload();
        });
        event.preventDefault();
    });
    $(document).on('submit','#remove_item', function(event) {
        $.ajax({
            data : {
                'item_id': $('#remove_item_id').val(),
                'quantity': $('#remove_item_quantity').val()
            },
            type : 'POST',
            url : '/remove_item'
        }).done(function(data) {
            location.reload();
        });
        event.preventDefault();
    });
} );