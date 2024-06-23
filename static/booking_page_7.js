const handleButton = (action) => {
  if (action == 'cancel') {
    if (confirm('Apakah kamu yakin ingin membatalkan booking?')) {
      let userData = JSON.parse(localStorage.getItem('userData'));
      let userId = userData.userId;
      $.ajax({
        type: 'POST',
        url: `/api/v1/cancel_order/${userId}`,
        success: function (res) {
          alert(res.msg);
          window.location.href = '/booking/8';
        },
      });
    }
  } else if (action == 'prev') {
    window.location.href = '/booking/6';
  }
};
