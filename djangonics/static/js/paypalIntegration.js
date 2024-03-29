$(function() {
    //render the buttons
    let totalValue = parseFloat($('#order-total').data('value')).toFixed(2);
    let authorizationID;
    let orderId;
    function initPayPalButtons() {
        paypal.Buttons({
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value: totalValue,
                        },
                    }],
                    application_context: {
                        shipping_preference: 'NO_SHIPPING',
                    }
                })
            },
            onApprove: function(data, actions) {
                return actions.order.get().then(function(details) {
                    orderId = details.id;
                    let csrfToken = $('#payment-selection-partial form input[name=csrfmiddlewaretoken]').val();

                    $.ajax({
                        url: '/accounts/select_payment_method/',
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                        },
                        data: {

                        },
                        success: function(data) {
                            $('#payment-selection').find('h5').hide();
                            $('#payment-selection').html(data);
                            $('#order-review h5').hide();
                            $('#order-review div.disabled-bg').show();
                            //Make an authorization request
                            $.ajax({
                                url: '/transactions/authorize_payment/',
                                type: 'POST',
                                headers: {
                                    'X-CSRFToken': csrfToken,
                                },
                                data: {
                                    order_id: orderId,
                                },
                                success: function(data) {
                                    //Show the order review section
                                    authorizationID = data['purchase_units'][0]['payments']['authorizations'][0]['id']
                                    $('#order-review div.disabled-bg').hide();
                                    $('#order-review h5').show();
                                    $('#order-review h5').css('color', '#007fff');
                                    $('#order-review-partial').slideDown(500, function() {
                                        $(this).show();
                                        $('.place-order-button').removeClass('disabled');
                                    });
                                },
                            });
                        }
                    });

                    $('.place-order-button').on('click', function(event) {
                        event.preventDefault();
                        //Make a call to the place_order view
                        $.ajax({
                            url: '/transactions/capture_payment/',
                            type: 'POST',
                            headers: {
                                'X-CSRFToken': csrfToken,
                            },
                            data: {
                                order_id: orderId,
                                authorization_id: authorizationID,
                                order_amount: totalValue,
                            },
                            success: function(data) {
                                //Make an AJAX request to the place_order view
                                $.ajax({
                                    url: '/transactions/place_order/',
                                    type: 'POST',
                                    headers: {
                                        'X-CSRFToken': csrfToken,
                                    },
                                    data: {
                                        order_id: orderId,
                                        total_amount: totalValue,
                                    },
                                    success: function(data) {

                                    },
                                    error: function(data) {
                                        alert('Something went wrong with your order.');
                                    }
                                });

                            },
                            error: function(data) {
                                alert('An error occurred.');
                            }
                        });
                    });
                });
            }
        }).render('#paypal-buttons-container');
    }
    initPayPalButtons();
})