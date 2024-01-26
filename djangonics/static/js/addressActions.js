$(function() {
    console.log("setDefaultAddress loaded");
     $('#add-address').on('click', function() {
        // Get the form data
        let formData = $('#modal-form form').serializeArray();

        console.log(formData);

        // Send an AJAX POST request to the server
        $.ajax({
          type: 'POST',
          url: '/accounts/add_address/',
          data: formData,
          success: function(data) {
            // Clear the form
                $('#modal-form form')[0].reset();
                $('#address-list-partial').append(data);
          }
        });
    });
    $('#addresses').on('click', '.set-default', function(event) {
        event.preventDefault();
        let addressId = $(this).closest('.address-action-form').data('address-id');
        $.ajax({
            url: `/accounts/set_default_address/${addressId}/`,
            type: 'POST',
            data: {
                address_id: addressId,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                $('#address-list-partial').replaceWith(data);
            }
        });
    });
    $('#addresses').on('click', '.remove-address', function(event) {
        event.preventDefault();
        let addressId = $(this).closest('.address-action-form').data('address-id');
        $.ajax({
            url: `/accounts/remove_address/${addressId}/`,
            type: 'POST',
            data: {
                address_id: addressId,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {
                 $('#address-list-partial').replaceWith(data);
            }
        });

    });
    $('#address-list-partial').on('click', '.edit-address', function(event) {
        event.preventDefault();
        let addressId = $(this).closest('.address-action-form').data('address-id');
        $.ajax({
            url: `/accounts/edit_address/${addressId}/`,
            type: 'GET',
            success: function(data) {
                 $('#edit-address-modal-form .modal-body').html(data);
                 $('#edit-address-modal-form').modal('show');
            }
        });
    });
    $('#save-changes').on('click', function(event) {
        event.preventDefault();
        let addressId = $('#edit-address-form input[name=id]').val();
        let formData = $('#edit-address-form').serializeArray();
        $.ajax({
            type: 'POST',
            url: `/accounts/save_address_changes/`,
            data: formData,
            success: function(data) {
                $(`#address-card-${addressId}`).replaceWith(data);
            }
        })
    })

});
