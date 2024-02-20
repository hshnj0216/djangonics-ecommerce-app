$(document).ready(function() {
    // Disable the submit button initially
    $('input[type="submit"]').prop('disabled', true);

    // Function to check if all fields are valid
    function checkValid() {
        var isValid = true;
        var firstName = $('#id_first_name').val();
        var lastName = $('#id_last_name').val();
        var email = $('#id_email').val();
        var contactNumber = $('#id_contact_number').val();
        var password = $('#id_password').val();

        // Validate first name
        if (!firstName || firstName.length > 100 || !firstName.replace(" ", "").match(/^[a-zA-Z]*$/)) {
            isValid = false;
        }

        // Validate last name
        if (!lastName || lastName.length > 100 || !lastName.replace(" ", "").match(/^[a-zA-Z]*$/)) {
            isValid = false;
        }

        // Validate email
        if (!email || !email.includes("@")) {
            isValid = false;
        }

        // Validate contact number
        if (!contactNumber || !contactNumber.match(/^(1-)?\d{3}-\d{3}-\d{4}$/)) {
            isValid = false;
        }

        // Validate password
        if (!password || password.length < 8 || password.includes(" ") || !password.match(/^[a-zA-Z0-9]*$/)) {
            isValid = false;
        }

        return isValid;
    }

    // Enable the submit button if all fields are valid
    $('form input').keyup(function() {
        if (checkValid())
            $('input[type="submit"]').prop('disabled', false);
        else
            $('input[type="submit"]').prop('disabled', true);
    });
});
