$(document).ready(function() {
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

    function htmlEncode(value){
      return $('<div/>').text(value).html();
    }

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
            url : '/request_item',
            error: function(xhr){
                    if(xhr.status == 405){
                        alert("You must be logged in to make request hardware")
                    }
                    $("#request_loading").css("display", "none");
                    event.preventDefault();
                }
        }).done(function(data) {
            location.reload();
        });
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
        // tracking lists for cart combination
        var cart_contents = []
        var cart_contents_ids = []

        // if the cart is empty
        if($("#cart")[0].childNodes[0].textContent === 'No items in cart'){
            // remove the placeholder text
            $("#cart")[0].removeChild($("#cart")[0].childNodes[0])
        }
        // number of items in the cart
        var cart_length = $("#cart")[0].childNodes.length;
        console.log($("#cart")[0].childNodes)

        // get the each item and its ID
        for(i = 0; i < cart_length; i+=3){
            cart_contents.push($("#cart")[0].childNodes[i]);
            cart_contents_ids.push($("#cart")[0].childNodes[i].id);
        }

        // item name
        var product_name = $(this)[0][1].value;
        // number of the item added to the cart
        var requested_quantity = $(this)[0][0].value;
        // amount in inventory
        var max_quantity = $(this)[0][0].max;

        var matched_index = cart_contents_ids.indexOf(product_name);
        if(matched_index != -1){
            var cur_quant = parseInt(cart_contents[matched_index].childNodes[2].value);
            var r_quant = parseInt(requested_quantity)
            console.log((cur_quant + r_quant))
            console.log(max_quantity)
            if((cur_quant + r_quant) <= parseInt(max_quantity)){
                cart_contents[matched_index].childNodes[2].value = cur_quant +
                                                                   r_quant;
            }else{
                var w_alert = "You have attempted to add " + 
                              (cur_quant + r_quant) + " " + product_name + 
                              "(s) to your cart, but only " + max_quantity +
                              " of them are in stock, we are sorry for this" + 
                              " inconvenience."
                window.alert(w_alert);
            }
            $('#cart').empty()
            for(i = 0; i < cart_contents.length; i++){
                $('#cart').append(cart_contents[i]);
                $('#cart').append('<br><br>')
            }
        }else{
            if(requested_quantity == ''){
                requested_quantity = 1;
            }

            var cart_item = '<li id="' + product_name + 
                            '"><strong id="prod_name">' + 
                            htmlEncode(product_name) + 
                            '</strong><button class=" btn-info cart-btn">X' + 
                            '</button><input type="number" name="item_quanity"' + 
                            'min="1" max="' + max_quantity + '" value="' +
                            requested_quantity + '" id="product_quantity"' +
                            ' required></li><br><br>'

            $('#cart').append(cart_item)
        }
        $(this)[0].reset()

        console.log(cart_contents)

        event.preventDefault();
    });

    $(document).on('submit','#cart-form', function(event) {
        if($(this)[0].childNodes[1].childNodes[0].data === 'No items in cart'){
            alert("To submit a hardware request you must add items to your cart");
        }else{
            $("#cart_loading").css("display", "inline-block");
            var items = [];
            var cart_length = $(this)[0].childNodes[1].childNodes.length;
            $('#confirm-request').empty()
            for(i = 0; i < cart_length; i += 3){
                var item = $(this)[0].childNodes[1].childNodes[i];

                var item_name = item.id;
                var item_quantity = item.childNodes[2].value;

                var formatted_item = '<li align="left">' + 
                                     '<span id="confirm-quantity">' +
                                     item_quantity + 'x </span>' +
                                     '<span id="con-item">' + 
                                     htmlEncode(item_name) + 
                                     '</span></li><br><br><br>'
                $('#confirm-request').append(formatted_item)

                items.push([htmlEncode(item_name), item_quantity])
            }
            $.ajax({
                data : {
                    'items': items
                },
                type : 'POST',
                url : '/submit_request',
                error: function(xhr){
                    $("#cart_loading").css("display", "none");
                    if(xhr.status == 405){
                        alert("You must be logged in to make a hardware request")
                    }
                    event.preventDefault();
                }
            }).done(function(data) {
                $("#cart_loading").css("display", "none");
                console.log(data)
                var r_id = data.id
                if(!(data.failed.join('') === '')){
                    var failed_items = [];
                    for(i = 0; i < data.failed.length; i++){
                        var failed_item = data.failed[i];
                        var formatted_failed_item = '<li>' + 
                            '<span style="float: left; color: grey">' +
                            failed_item.quantity + 'x</span>' + 
                            '<span style="align-text: left;">' +
                            htmlEncode(failed_item.name) + 
                            '</span></p><hr><br></li>'
                        failed_items.push(formatted_failed_item);
                    }
                    var failed_message = '<h4>We were unable to checkout the' +
                                         ' following items</h4>' + 
                                         failed_items.join(' ')
                    $('#failed-items').append(failed_message)
                }
                var confirmation_message = 'Your request ID is "<u>' + 
                                            htmlEncode(r_id) + 
                                           '</u>". You will be notified when it' +
                                           ' is ready for pickup.'
                $('#confirm-message').append(confirmation_message)
                console.log(items);
                document.getElementById("overlay").style.display = "block";
            });
        }
        event.preventDefault();
    });

    $(document).on('click', '#confirm-exit', function(event){
        document.getElementById("overlay").style.display = "none";
        window.location.reload();
    });

} );