$(function() {
    console.log('checkoutActionsHandler.js loaded');
    $('#use-this-address-button').on('click', function(event) {
        event.preventDefault();
        let selectedAddressId = $('input[name="address"]:checked').val();
        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: 'POST',
            url: `/accounts/use_address/`,
            data: {
                address_id: selectedAddressId,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                let address = data['address'];
                $('#address-selection').replaceWith(data)
            }
        })
    })
});