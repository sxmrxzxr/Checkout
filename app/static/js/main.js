$(document).ready(function() {
    console.log("HERE")
    $('#inventory').DataTable({
        "paging": false,
        "autoWidth": false,
        "scrollY": "75%",
        "scrollCollapse": true,
        "columnDefs": [
            { "width": "20%", "targets": 0 }
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
    $(document).on('submit','#request_item', function(event) {
        $("#request_loading").css("display", "inline-block");
        $.ajax({
            data : {
                'name': $('#request_name').val(),
                'email': $('#request_email').val(),
                'item': $('#request_item_name').val(),
                'content': $('#request_desc').val()
            },
            type : 'POST',
            url : '/request_item'
        }).done(function(data) {
            location.reload();
        });
        $('#request_item')[0].reset();
        event.preventDefault();
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
        $('#add_hackathon')[0].reset();
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
        $('#remove_hackathon')[0].reset();
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
        $('#add_item')[0].reset();
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
        $('#increase_quantity')[0].reset();
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
        $('#remove_item')[0].reset();
        event.preventDefault();
    });

    $(document).on('submit','#add-to-cart', function(event) {
        var cart_contents = []
        var i = 0;
        var cart_length = $("#cart")[0].childNodes.length;

        for(i = 1; i < cart_length; i+=3){
            cart_contents.push($("#cart")[0].childNodes[i]);
        }

        console.log(cart_contents)

        var product_name = $(this)[0][1].value;
        var requested_quantity = $(this)[0][0].value;
        var max_quantity = 4;
        
        if(requested_quantity == ''){
            requested_quantity = 1;
        }

        var cart_item = '<li id="' + product_name + 
                        '"><strong id="prod_name">' + product_name + 
                        '</strong><button class=" btn-info cart-btn">X' + 
                        '</button><input type="number" name="item_quanity"' + 
                        'min="1" max="' + max_quantity + '" value="' +
                        requested_quantity + '" id="product_quantity"' +
                        ' required></li><br><br>'

        $('#cart').append(cart_item)

        event.preventDefault();
    });

} );