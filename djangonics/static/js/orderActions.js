import { loadImages } from './loadImages.js';
$(function() {
    console.log('order actions loaded');
    //Handle the cancel order event
    const cancelOrderBtns = $('.cancel-order-btn');
    const cancelOrderConfirmBtn = $('#cancel-order-confirm');

    let selectedOrderId;

    cancelOrderBtns.on('click', function() {
        selectedOrderId = $(this).data('order-id');
    });

    cancelOrderConfirmBtn.on('click', function() {
        $.ajax({
            url: `/transactions/cancel_order/${selectedOrderId}/`,
            method: 'POST',
            success: function(data) {
                // Handle successful cancellation
                $('#orders-container').html(data);
            },
            error: function() {
                // Handle error

            }
        });
    });

    //Handle the order status filtering
    $('#order-status').on('change', function() {
        let status = $(this).val();
        $.get(
            '/transactions/filter_orders/',
            {status},
            function(data) {
                $('#orders-container').html(data);
                loadImages('high');
            }
        );
    });
});
