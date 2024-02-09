
$(function() {
    console.log('checkoutActionsHandler.js loaded');
    //hide preloaded order items review partial and highlight current phase
    $('#payment-selection-partial').hide();
    $('#order-review-partial').hide();
    $('.disabled-bg').hide();
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

                $('#address-selection').slideUp(300, function() {
                    $(this).html(data['selected_address_html']).slideDown(300);
                });
                $('#payment-selection-partial').slideDown(500, function() {
                    $(this).show();
                    $(this).siblings('h5').text('2. Select a payment method');
                    $(this).siblings('h5').css('color', '#007fff');
                });
            }
          });
        } catch (error) {
          // Handle error
          console.log('An error occurred:', error);
        }
    });

    //change address handler
    $('#address-selection').on('click', '#change-address-button', function(event) {
        event.preventDefault();
        let csrfToken = $('#address-selection form input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'POST',
            url: '/accounts/change_selected_address/',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function(data) {
                $('#order-review-partial').slideUp(300, function() {
                    $(this).hide();
                    $('#order-review h5').text('3. Review order').css('color', '#000000');
                });
                $('#payment-selection-partial').slideUp(300, function() {
                    $(this).hide();
                    $('#payment-selection h5').text('2. Payment selection').css('color', '#000000');
                });
                $('#address-selection').slideUp(300, function() {
                    $(this).html(data).slideDown(500);
                    $('#address-selection h5').css('color', '#007fff');
                });

            }
        });
    });
    //handle address addition
    $('#add-address').on('click', function() {
        // Get the form data
        let formData = $('#add-address-modal-form form').serializeArray();

        console.log(formData);

        // Send an AJAX POST request to the server
        $.ajax({
          type: 'POST',
          url: '/accounts/add_address_from_checkout/',
          data: formData,
          success: function(data) {
            // Clear the form
                $('#add-address-modal-form form')[0].reset();
                $('#address-list-form').append(data);
          }
        });
    });
    //handle edit address button click
    $('.edit-address').on('click', function(event) {
        let addressId = $(this).data('address-id');
         $.ajax({
            url: `/accounts/edit_address/${addressId}/`,
            type: 'GET',
            success: function(data) {
                 $('#edit-address-modal-form .modal-body').html(data);
                 $('#edit-address-modal-form').modal('show');
            }
        });
    });

    //handle edit address submission
    $('#save-changes').on('click', function(event) {
        event.preventDefault();
        let addressId = $('#edit-address-form input[name=id]').val();
        let formData = $('#edit-address-form').serializeArray();
        $.ajax({
            type: 'POST',
            url: `/accounts/save_address_changes_from_checkout/`,
            data: formData,
            success: function(data) {
                $(`#address-entry-${addressId}`).replaceWith(data);
            }
        })
    })



});