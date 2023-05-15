$(function() {
    console.log("setDefaultAddress loaded");
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
    $('#addresses').on('click', '.edit-address', function(event) {
        event.preventDefault();
        let addressId = $(this).closest('.address-action-form').data('address-id');
        $.ajax({
            url: `/accounts/edit_address/${addressId}/`,
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
});
