$(function() {
    $('#add-address').on('click', function() {
        // Get the form data
        let formData = {
          'full_name': $('#full-name').val(),
          'address_line_1': $('#address-line-1').val(),
          'address_line_2': $('#address-line-2').val(),
          'city': $('#city').val(),
          'state': $('#state').val(),
          'zip': $('#zip').val(),
          'phone_number': $('#number').val(),
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        };

        // Send an AJAX POST request to the server
        $.ajax({
          type: 'POST',
          url: '/accounts/add_address/',
          data: formData,
          success: function(data) {
            if(data['success']) {
                // Clear the form
                $('#modal-form form')[0].reset();
                $('#address-list').append(`
                    <div class="address col-3 p-3 m-2 border rounded">
                        <h6>${formData.full_name}</h6>
                        <p>${formData.address_line_1}, ${formData.address_line_2}</p>
                        <p>${formData.city}, ${formData.state} ${formData.zip}</p>
                        <p>United States</p>
                        <p>Phone number: ${formData.phone_number}</p>
                        <ul class="list-unstyled d-flex">
                            <li class="address-action">Edit</li>
                            <li class="address-action">Remove</li>
                            <li class="address-action">Set as Default</li>
                        </ul>
                    </div>
                `);
            }
          }
        });
    });
});
