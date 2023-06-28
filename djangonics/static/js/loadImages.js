$(function() {
    console.log('loadImages.js loaded');
    let images = $('.product-img');
    images.each(function() {
        let image = $(this);
        let imgSrc = image.data('src-high');
        $.get(imgSrc, function(data){
            image.attr('src', data['img_urls'][0]);
        });
    });


});
