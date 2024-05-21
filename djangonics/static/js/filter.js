import { loadImages } from './loadImages.js';
$(function() {
    let url = $('.filter-form').data('filter-url');

    // function to update the product list via AJAX
    function updateProductList() {
        let selectedCategories = [];
        let minPrice = parseInt($('#min_price').val()) || 0;
        let maxPrice = parseInt($('#max_price').val()) || 9999;
        let currentPage = $('#content-container').data('page');
        let query = $('#content-container').data('query');
        let rating = $('.star-rating-filter.selected-rating').data('rating');

        // iterate over the checkboxes to get the selected categories
        $('.filter-form :checkbox:checked').each(function() {
            selectedCategories.push($(this).val());
        });

        // make an AJAX request with the selected categories, price range, and product IDs
        $.ajax({
            url: url,
            type: 'GET',
            data: {
                categories: selectedCategories.join(','),
                min_price: minPrice,
                max_price: maxPrice,
                rating: rating,
                current_page: currentPage,
                query
            },
            success: function(data) {
                $('#product-list-partial').html(data);
                loadImages('high');
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

    //attach event listener to the star rating div
    $('.star-rating-filter').on('click', function() {
        if($(this).hasClass('selected-rating')) {
            $(this).removeClass('selected-rating');
        } else {
            $('.star-rating-filter').each(function() {
                $(this).removeClass('selected-rating')
            });
            $(this).addClass('selected-rating');
        }
        updateProductList();
    });

    $('#clear-filters-btn').on('click', function() {
        $('#filter-form').trigger('reset');
    });
});
