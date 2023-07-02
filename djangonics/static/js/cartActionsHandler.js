$(function() {

    $('#checkout-button').prop('disabled', true);
    console.log("select all loaded");
    //toggle checking/unchecking of cart item checkboxes
    $('#select-all-check').on('change', function() {
        var isChecked = $(this).is(':checked');
        $('.cart-item-checkbox').prop('checked', isChecked);
    });

    //toggle disable/enable checkout button if no items are selected
    $('input[name="cart_item"], #select-all-check').on('change', function() {
        let cartItems = $('input[name="cart_item"]:checked');
        if(cartItems.length !== 0) {
            $('#checkout-button').prop('disabled', false);
            $('#checkout-button').removeClass('mb-1');
            $('#checkout-button').addClass('mb-3');
            $('#message').hide();
        } else {
            $('#checkout-button').prop('disabled', true);
             $('#checkout-button').removeClass('mb-3');
            $('#checkout-button').addClass('mb-1');
            $('#message').show();
        }
    });

});