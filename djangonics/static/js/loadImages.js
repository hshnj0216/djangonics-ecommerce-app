$(function() {
    let images = $('.product-img');
    images.each(function() {
        let imgSrc = $(this).data('src');
        $.get(imgSrc, function(data) {
            $(this).attr('src', data['img_urls']);
        }.bind(this));
    });
});
