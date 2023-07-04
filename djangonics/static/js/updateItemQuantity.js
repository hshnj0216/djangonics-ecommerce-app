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

    // Handle focus event on .cart-item-qty element
    $('.cart-item-options').on('focus', '.cart-item-qty', function() {
        if($(this).val() !== 'expand') {
            $(this).data('prev-value', $(this).val());
        }
    });

    //Restore prefilled value on blur
    $('.cart-item-options').on('blur', 'input.cart-item-qty', function() {
        let prevValue = $(this).data('prev-value');
        if($(this).val() === '') {
            $(this).val(prevValue);
        }
    });


    //toggle display of update button
    $('.cart-item-options').on('input', 'input.cart-item-qty', function() {
        console.log('changed');
        if($(this).val() === '') {
            $(this).closest('.cart-item-qty-container').find('.update-qty-button').addClass('d-none');
        } else {
            $(this).closest('.cart-item-qty-container').find('.update-qty-button').removeClass('d-none');
        }
    });

    // Handle change event on .cart-item-qty class
    $('.cart-item-options').on('change', '.cart-item-qty', function() {
        // Make an AJAX call to update the cart item count
        let qty = $(this).val();
        let productId = $(this).data('product-id');
        let topMostDiv = $(this).closest('.cart-card');
        let cartItemId = $(this).data('cart-item-id');

        if(parseInt(qty) === 0) {
            removeItem(qty, productId, cartItemId, topMostDiv);
        } else if(parseInt(qty) < 10) {
            updateCounter(qty, productId, cartItemId);
        } else if(qty === "expand") {
            // Show update button and use a number input instead of select
            let container = $(this).closest('.cart-item-qty-container');
            let price = $(this).data('price');
            let prevValue = $(this).data('prev-value');
            container.html(`
                <label class="me-1">Qty:
                    <input type="number"
                           class="cart-item-qty form-control-sm"
                           value=${prevValue}
                           data-price=${price}
                           data-product-id=${productId}
                           data-cart-item-id=${cartItemId}
                           data-prev-value=${prevValue}
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
        let inputElement = $(this).siblings('label').find('input.cart-item-qty');
        let qty = inputElement.val();
        if (qty === '') {
            qty = inputElement.data('prev-value');
        }
        let productId = inputElement.data('product-id');
        let cartItemId = inputElement.data('cart-item-id');
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
