$(function() {
    //if the quantity and selected items change, calculate the price
    // Get the elements that we will be working with
    console.log("calculatePrice loaded");
    let checkboxes = $('.cart-item-checkbox');
    let quantities = $('.cart-item-qty');
    let selectAllCheck = $('#select-all-check');
    // Function to calculate the total price
    function calculateSubTotalPrice() {
        let subTotalPrice = 0;
        let itemCount = 0;
        checkboxes.each(function(index, checkbox) {
            if (checkbox.checked) {
                let quantityContainer = quantities.eq(index);
                let price = parseFloat(quantityContainer.data('price'));
                let quantity = parseInt(quantityContainer.val());
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
    checkboxes.on('change', calculateSubTotalPrice);
    quantities.on('change', calculateSubTotalPrice);
    selectAllCheck.on('change', calculateSubTotalPrice);
});