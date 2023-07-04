$(function() {
    //if the quantity and selected items change, calculate the price
    // Get the elements that we will be working with
    console.log("calculatePrice loaded");

    // Function to calculate the total price
    function calculateSubTotalPrice() {
        let checkboxes = $('.cart-item-checkbox');
        let quantities = $('.cart-item-qty');
        let selectAllCheck = $('#select-all-check');
        let subTotalPrice = 0;
        let itemCount = 0;
        checkboxes.each(function(index, checkbox) {
            if (checkbox.checked) {
                let quantityContainer = quantities.eq(index);
                let price = parseFloat(quantityContainer.data('price'));
                console.log(price);
                let quantity = parseInt(quantityContainer.val());
                console.log(`quantity: ${quantity}`);
                itemCount += quantity;
                subTotalPrice += price * quantity;
            }
        });
        $('#subtotal-price').text(subTotalPrice.toFixed(2));
        $('#item-count').text(itemCount);
    }

    // Calculate subtotal price on page load
    calculateSubTotalPrice();

    // Listen for changes to the checkboxes and selects
    $('.cart-item-checkbox').on('change', calculateSubTotalPrice);
    $('.cart-item-options').on('change', '.cart-item-qty', calculateSubTotalPrice);
    $('#select-all-check').on('change', calculateSubTotalPrice);
});