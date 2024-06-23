$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/pengajuan_cuti',
    data: {},
    success: function (res) {
      console.log(res.result);
    },
  });
});
