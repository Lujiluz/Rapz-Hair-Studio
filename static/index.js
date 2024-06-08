$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_user?role=admin',
    data: {},
    success: function (response) {
      console.log(response);
    },
  });
});

const handleTestimonials = () => {
  let name = $('#name').val();
  let rating = $('input[name="rating"]:checked').val();
  let review = $('#review').val();

  $.ajax({
    type: 'POST',
    url: '/api/v1/add_testimoni',
    data: {
      name,
      rating,
      review,
    },
    success: function (response) {
      alert(response.result);
    },
  });
};
