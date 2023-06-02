$(function() {
    console.log('checkoutActionsHandler.js loaded');
    //handles address selection
    $('#address-selection h5').css('color', '#007fff');
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
                $('#payment-selection').hide().html(data['payment_selection_html']).slideDown(500);
                $('#payment-selection h5').css('color', '#007fff');
            }
          });
        } catch (error) {
          // Handle error
          console.log('An error occurred:', error);
        }
    });
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
            }
        });
    });

    //handle the payment select event
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
            }
        });
    });
});