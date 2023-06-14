$(function() {
    console.log("updateItemQuantity loaded");

    function removeItem(productId, cartItemId, topMostDiv) {
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
    }

    function updateCounter(qty, productId, cartItemId) {
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

    //update item quantity if quantity is less than 10
    $('.cart-item-options').on('change', '.cart-item-qty', function() {
        // Make an AJAX call to update the cart item count
        let qty = $(this).val();
        let productId = $(this).data('product-id');
        let topMostDiv = $(this).closest('.cart-card');
        let cartItemId = $(this).data('cart-item-id');

        updateCounter(qty, productId, cartItemId);

        if(qty < 10 && qty != 0) {
            updateCounter(qty, productId, cartItemId);
        } else if(qty == 0) {
            removeItem(productId, cartItemId, topMostDiv);
        } else {
            //show update button and use a number input instead of select
            let container = $(this).closest('.cart-item-qty-container');
            let price = $(this).data('price');
            container.html(`
                <label class="me-1">Qty:
                    <input type="number"
                           class="cart-item-qty"
                           maxlength="999"
                           value=""
                           data-price=${price}
                           data-product-id=${productId}
                           data-cart-item-id=${cartItemId}
                    >
                </label>
                <button class="btn btn-sm btn-primary update-qty-button d-none">Update</button>
            `);
            container.find('button').removeClass('d-none');
        }
    });

    //handle the update button click event
    $('.cart-item-options').on('click', '.update-qty-button', function() {
        let qty = $(this).prev('label').find('.cart-item-qty').val();
        let productId = $(this).prev('label').find('.cart-item-qty').data('product-id');
        let cartItemId = $(this).prev('label').find('.cart-item-qty').data('cart-item-id');
        updateCounter(qty, productId, cartItemId);
        let inputElement = $(this).prev('label').find('.cart-item-qty');
        inputElement.val(qty);
        $(this).addClass('d-none');
        $(this).attr('random', 'random');
    });

    //handle remove button click event
     $('.remove-item-btn').on('click', function() {
        let productId = $(this).data('product-id');
        let cartItemId = $(this).data('cart-item-id');
        let topMostDiv = $(this).closest('.cart-card');
        removeItem(productId, cartItemId, topMostDiv);
     });

});