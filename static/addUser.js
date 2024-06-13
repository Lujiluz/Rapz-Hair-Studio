$(document).ready(function () {
  // function agar gambar yang di-upload langsung ditampilkan sebagai preview
  $('#profile_image').change(function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        $('#preview_img').attr('src', e.target.result).show();
      };
      reader.readAsDataURL(file);
    } else {
      $('#preview_img').hide();
    }
  });
});

const handleSubmit = () => {
  const formData = new FormData();
  const profileImage = $('#profile_image')[0].files[0];
  if (profileImage) formData.append('profile_img', profileImage);

  formData.append('fullName', $('#fullName').val());
  formData.append('email', $('#email').val());
  formData.append('password', $('#password').val());
  formData.append('waNum', $('#waNum').val());
  formData.append('pricePerService', $('#service-price').val());
  formData.append('role', $('#role').val());

  $.ajax({
    type: 'POST',
    url: '/api/v1/add_user',
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      console.log(response.result);
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log('Error:', textStatus, errorThrown);
    },
  });
};
