const sidebarToggle = document.querySelector('#sidebar-toggle');
sidebarToggle.addEventListener('click', function () {
  document.querySelector('#sidebar').classList.toggle('collapsed');
});

// for datepicker
document.addEventListener('DOMContentLoaded', function () {
  // instance flatpickr tgl awal
  flatpickr('#datetimepickerInput', {
    enableTime: false,
    dateFormat: 'd/m/Y',
  });

  document.querySelector('.input-group-text').addEventListener('click', function () {
    document.querySelector('#datetimepickerInput')._flatpickr.open();
  });

  let nama = $('#nama').text();
  $.ajax({
    type: 'GET',
    url: `/api/v1/data_pengajuan_cuti?nama=${nama}`,
    data: {},
    success: function (res) {
      if (res.dataPengajuan.length > 0) {
        res.dataPengajuan.map((pengajuan) => {
          let htmlDataPengajuan = `  <tr>
                                      <td>${pengajuan.tglAwal}</td>
                                      <td>${pengajuan.tglAkhir}</td>
                                      <td>${pengajuan.alasanCuti}</td>
                                      <td>
                                        <div class="bg-primary rounded text-white mx-3 w-auto">
                                          <p class="py-1 px-2" id="status-text">${pengajuan.status}</p>
                                        </div>
                                      </td>
                                    </tr>`;
          $('#data-cuti').append(htmlDataPengajuan);
        });
      } else {
        $('#leaveTable').hide();
      }
    },
  });
});

// handle button pengajuan cuti
const handleSubmitPengajuanCuti = () => {
  let nama = $('#nama-hairstylist').val();
  let dates = document.querySelectorAll('#datetimepickerInput');
  let tglAwal = dates[0].value;
  let tglAkhir = dates[1].value;
  let alasanCuti = $('#alasan-cuti').val();
  console.log(nama);

  $.ajax({
    type: 'POST',
    url: '/api/v1/pengajuan_cuti',
    data: {
      nama,
      tglAwal,
      tglAkhir,
      alasanCuti,
    },
    success: function (res) {
      alert(res.msg);
      location.reload();
    },
  });
};

// handle logout
const handleLogout = () => {
  if (confirm('Yakin mau logout, a?')) {
    $.removeCookie('token', null, { path: '/admin' });
    window.location.href = '/admin/login';
  }
};
