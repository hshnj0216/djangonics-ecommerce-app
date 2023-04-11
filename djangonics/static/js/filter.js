$(function() {
    //attach a change event listener to the checkboxes of the filter form
    $('.filter-form').change(function() {
        console.log("checked/unchecked");
        let url = $(this).data('filter-url')
        let selectedCategories = [];

        //iterate over the checkboxes to get the selected categories
        $('.filter-form :checkbox:checked').each(function() {
            selectedCategories.push($(this).val());
        });

        //make an AJAX request
        $.ajax({
                url:url,
            data: {
                categories: selectedCategories.join(',')
            },
            success: function(data) {
                $('#product-list-partial').html(data);
            }
        });
    });
});