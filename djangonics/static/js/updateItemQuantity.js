$(function() {
    console.log("updateItemQuantity loaded");

    //update item quantity if quantity is less than 10
    $('.cart-item-options').on('change', '.cart-item-qty', function() {
        // Make an AJAX call to update the cart item count
        let qty = $(this).val();
        let productId = $(this).data('product-id');
        let topMostDiv = $(this).closest('.cart-card');
        let cartItemId = $(this).data('cart-item-id');

        function updateCounter(qty, productId) {
            $.ajax({
                url: '/products/update_item_quantity/',
                type: 'POST',
                data: {
                    qty,
                    product_id: productId,
                    cart_item_id: cartItemId,
                },
                success: function(data) {
                    // Update the cart item count in the navbar
                    $('#item-counter').text(data.cart_item_count);
                }
            });
        }

        if(qty < 10 && qty != 0) {
            updateCounter(qty, productId);
        } else if(qty == 0) {
            $.ajax({
                url: `/products/remove_item/${productId}/${cartItemId}/`,
                data: {
                    product_id: productId,
                    cart_item_id: cartItemId,
                },
                type: 'POST',
                success: function(data) {
                    topMostDiv.replaceWith(data);
                }
            });
        } else {
            //show update button and use a number input instead of select
            let container = $(this).closest('.cart-item-qty-container');
            container.html(`
                <label>Qty:
                    <input type="number"
                           class="cart-item-qty"
                           value=${qty}
                           data-price=""
                           data-product-id=""
                    >
                    <button class="btn btn-primary update-button d-none">Update</button>
                </label>
            `);
            container.find('button').removeClass('d-none');
        }


    });

});