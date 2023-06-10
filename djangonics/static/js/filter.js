$(function() {
    let url = $('.filter-form').data('filter-url');

    // function to update the product list via AJAX
    function updateProductList() {
        let selectedCategories = [];
        let minPrice = parseInt($('#min_price').val()) || 0;
        let maxPrice = parseInt($('#max_price').val()) || 9999;
        let productIds = [];

        // iterate over the checkboxes to get the selected categories
        $('.filter-form :checkbox:checked').each(function() {
            selectedCategories.push($(this).val());
        });

        // iterate over the product elements to get their IDs
        $('.product').each(function() {
            productIds.push($(this).data('product-id'));
        });

        // make an AJAX request with the selected categories, price range, and product IDs
        $.ajax({
            url: url,
            data: {
                categories: selectedCategories.join(','),
                min_price: minPrice,
                max_price: maxPrice,
                product_ids: productIds.join(',')
            },
            success: function(data) {
                $('#product-list-partial').html(data);
            }
        });
    }

    // attach a change event listener to the checkboxes of the filter form
    $('.filter-form :checkbox').change(function() {
        updateProductList();
    });

    // attach a submit event listener to the filter form to prevent default submit behavior
    $('.filter-form').submit(function(event) {
        event.preventDefault();
        updateProductList();
    });
});
