$(function() {
    console.log('checkoutActionsHandler.js loaded');
    //hide preloaded order items review partial and highlight current phase
    $('#payment-selection-partial').hide();
    $('#order-review-partial').hide();
    $('#address-selection h5').css('color', '#007fff');

    //use address button handler
    $('#address-selection').on('click', '#use-this-address-button', function(event) {
        event.preventDefault();
        let selectedAddressId = $('input[name="address"]:checked').val();
        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        try {
          // Make AJAX request to use_address endpoint
          $.ajax({
            type: 'POST',
            url: '/accounts/use_address/',
            data: {
                address_id: selectedAddressId,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                $('#address-selection h5').css('color', '#000000');
                $('#address-selection').slideUp(300, function() {
                    $(this).html(data['selected_address_html']).slideDown(300);
                });
                $('#payment-selection-partial').slideDown(500, function() {
                    $(this).show();
                    $(this).siblings('h5').text('2. Select a payment method').css('color', '#007fff');
                });
            }
          });
        } catch (error) {
          // Handle error
          console.log('An error occurred:', error);
        }
    });

    //proceed to payment handler
    $('#order-review').on('click', '#proceed-to-payment-button', function(event) {
        event.preventDefault();
        //hide the section and show the payment section
        $(this).closest('#order-review').slideUp(300, function() {

        });
    })

    //change address handler
    $('#address-selection').on('click', '#change-address-button', function(event) {
        event.preventDefault();
        console.log('Change address');
        let csrfToken = $('#address-selection form input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'POST',
            url: '/accounts/change_selected_address/',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                $('#payment-selection').slideUp(500, function() {
                    $(this).html(`
                        <h5>2. Payment method</h5>
                    `).slideDown(300);
                });
                $('#address-selection').slideUp(300, function() {
                    $(this).html(data).slideDown(500);
                    $('#address-selection h5').css('color', '#007fff');
                });
                $('#order-review-partial').slideUp(300, function() {
                    $(this).hide();
                    $('#order-review h5').text('3. Review order').css('color', '#000000');

                });
            }
        });
    });

    //payment method selection handler
    $('#payment-selection').on('click','#use-this-payment-method-button', function(event) {
        event.preventDefault();
        let csrfToken = $('#payment-selection form input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'POST',
            url: '/accounts/select_payment_method/',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                $('#payment-selection').slideUp(300, function() {
                    $(this).html(data).slideDown(500);
                });
                $('#order-review h5').text('3. Review your order').css('color', '#007fff');
                $('#order-review-partial').slideDown(500, function() {
                    $(this).show();
                });
            }
        });
    });
});