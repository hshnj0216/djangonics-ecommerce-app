$(function() {
    let url = $('#search').data('search-url');
    $('#search').submit(function(event) {
        event.preventDefault();
        let category = $('#category-selection').val();
        let queryString = $('#query').val();

        $.ajax({
            url: url,
            data: {
                query_string: queryString,
            },
            success:function(data) {
                $('#product-list-partial').html(data);
            }
        })
    });

});