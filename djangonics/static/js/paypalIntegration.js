$(function() {
    //render the buttons
    console.log('Paypal integration script loaded');
    let totalValue = parseFloat($('#order-total').data('value')).toFixed(2);
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
                    console.log(details);
                    let orderId = details.id;
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
                        }
                    })

                    //Show the order review sections
                    $('#order-review-partial').slideDown(500, function() {
                        $(this).siblings('h5').css('color', '#007fff');
                        $(this).show();
                    });

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
                            console.log(data);
                        },

                    });

                });
            }
        }).render('#paypal-buttons-container');
    }
    initPayPalButtons();
})