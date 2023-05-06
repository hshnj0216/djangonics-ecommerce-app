$(function() {
    console.log("updateItemQuantity loaded");
    function updateCounter(qty, productId, token) {
        console.log(token);
        $.ajax({
            url: '/products/update_item_quantity/',
            type: 'POST',
            data: {
                qty,
                product_id: productId,
                csrfmiddlewaretoken: token,
            },
            success: function(data) {
                // Update the cart item count in the navbar
                $('#item-counter').text(data.cart_item_count);
            }
        });
    }
    $('.cart-item-select').on('change', function() {
        // Make an AJAX call to update the cart item count
        let qty = $(this).val();
        let productId = $(this).data('product-id');
        let token = $(this).siblings("input[name='csrfmiddlewaretoken']").val();
        updateCounter(qty, productId, token);
    });
});