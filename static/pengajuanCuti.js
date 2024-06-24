$(document).ready(function () {
    // Initialize flatpickr
    $('.datepicker').flatpickr({
        dateFormat: 'Y-m-d'
    });

    const apiUrl = '/';

    // Submit leave request form
    $('#leaveForm').submit(function (event) {
        event.preventDefault();
        const formData = {
            user_id: $('#user_id').val(),
            start_date: $('#start_date').val(),
            end_date: $('#end_date').val(),
            reason: $('#reason').val()
        };
        $.ajax({
            type: 'POST',
            url: apiUrl + 'leave',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function () {
                alert('Leave request submitted successfully');
                location.reload();
            }
        });
    });

    // Approve leave request
    $(document).on('click', '.approve-btn', function () {
        const leaveId = $(this).data('id');
        $.ajax({
            type: 'PUT',
            url: apiUrl + `leave/${leaveId}/approve`,
            success: function () {
                alert('Leave request approved');
                location.reload();
            }
        });
    });

    // Reject leave request
    $(document).on('click', '.reject-btn', function () {
        const leaveId = $(this).data('id');
        $.ajax({
            type: 'PUT',
            url: apiUrl + `leave/${leaveId}/reject`,
            success: function () {
                alert('Leave request rejected');
                location.reload();
            }
        });
    });
});