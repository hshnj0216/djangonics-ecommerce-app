$(function() {
    console.log("updateItemQuantity loaded");

    // Function to update the cart item count
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
                $('#item-counter').text(data['cart_item_count']);
                let optionsContainer = $(`#${cartItemId} .cart-item-options`);
                optionsContainer.html(data['cart_item_options_html']);
            },
            error: function() {
                // Display an error message to the user
                console.log(productId);
                alert('An error occurred while updating the cart item count. Please try again.');
            }
        });
    }

    // Function to remove an item from the cart
    function removeItem(qty, productId, cartItemId, topMostDiv) {
        $.ajax({
            url: `/products/remove_item/`,
            data: {
                product_id: productId,
                cart_item_id: cartItemId,
            },
            type: 'POST',
            success: function(data) {
                topMostDiv.replaceWith(data['removed_html']);
                $('#item-counter').text(data['cart_item_count']);
            },
            error: function() {
                // Display an error message to the user
                alert('An error occurred while removing the item from the cart. Please try again.');
            }
        });
    }

    // Handle change event on .cart-item-qty element
    $('.cart-item-options').on('change', '.cart-item-qty', function() {
        // Make an AJAX call to update the cart item count
        let qty = $(this).val();
        let productId = $(this).data('product-id');
        let topMostDiv = $(this).closest('.cart-card');
        let cartItemId = $(this).data('cart-item-id');

        if(qty < 10 && qty != 0) {
            updateCounter(qty, productId, cartItemId);
        } else if(qty == 0) {
            removeItem(qty, productId, cartItemId, topMostDiv);
        } else if(qty == "10+") {
            // Show update button and use a number input instead of select
            let container = $(this).closest('.cart-item-qty-container');
            let price = $(this).data('price');
            container.html(`
                <label class="me-1">Qty:
                    <input type="number"
                           class="cart-item-qty form-control-sm"
                           maxlength="999"
                           value=""
                           data-price=${price}
                           data-product-id=${productId}
                           data-cart-item-id=${cartItemId}
                    >
                </label>
                <button type="button" class="btn btn-sm btn-primary update-qty-button ms-1 d-none">Update</button>
            `);
            container.find('button').removeClass('d-none');
        }
    });

    // Handle focus event on input.cart-item-qty element
    $('.cart-item-options').on('focus', 'input.cart-item-qty', function() {
        let button = $(this).parent().next('button.update-qty-button');
        button.removeClass('d-none');
    });

    // Handle click event on .update-qty-button element
    $('.cart-item-options').on('click', '.update-qty-button', function(event) {
        event.preventDefault();
        let qty = $(this).siblings('label').find('.cart-item-qty').val();
        let productId = $(this).siblings('label').find('.cart-item-qty').data('product-id');
        let cartItemId = $(this).siblings ('label').find('.cart-item-qty').data('cart-item-id');
        updateCounter(qty, productId, cartItemId);
        $(this).addClass('d-none');
    });

    // Handle click event on .remove-item-btn element
     $('.remove-item-btn').on('click', function() {
        let qty = $(this).data('qty');
        let productId = $(this).data('product-id');
        let cartItemId = $(this).data('cart-item-id');
        let topMostDiv = $(this).closest('.cart-card');
        removeItem(qty, productId, cartItemId, topMostDiv);
     });
});
