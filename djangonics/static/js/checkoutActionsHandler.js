$(function() {
    console.log('checkoutActionsHandler.js loaded');
    //handles address selection
    $('#use-this-address-button').on('click', function(event) {
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
                $('#address-selection').replaceWith(data['selected_address_html']);
                $('#payment-selection').replaceWith(data['payment_selection_html']);
            }
          });
        } catch (error) {
          // Handle error
          console.log('An error occurred:', error);
        }
      });
    //handle the payment select event
    /*$('#use-this-payment-method').on('click', function(event) {
        event.preventDefault();

    });
    */
});