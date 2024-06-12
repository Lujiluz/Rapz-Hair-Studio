const handleTestimoni = () => {
  let name = $('#name').val();
  let rating = $('#rating').val();
  let review = $('#review').val();

  $.ajax({
    type: 'POST',
    url: '/api/v1/add_testimoni',
    data: {
      name,
      rating,
      review,
    },
    beforeSend: function () {
      console.log('sending...');
    },
    success: function (res) {
      $('#name').val('');
      $('#rating').val('');
      $('#review').val('');
      alert('testimoni kamu terkirim!👌');
    },
    error: function (e) {
      alert('Maaf, kita lagi ada masalah di sistem..🙏🥹');
    },
  });
};
