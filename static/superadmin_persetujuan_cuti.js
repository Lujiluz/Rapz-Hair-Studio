$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/persetujuan_cuti',
    data: {},
    success: function (res) {
      res.data.map((pengajuan) => {
        let [tglAwal, bulanAwal, tahunAwal] = pengajuan.tglAwal.split('/');
        let [tglAkhir, bulanAkhir, tahunAkhir] = pengajuan.tglAkhir.split('/');
        let tglCuti = `${tglAwal} - ${tglAkhir}, ${bulanAwal == bulanAkhir ? bulanAwal : bulanAwal + '-' + bulanAkhir} ${tahunAwal == tahunAkhir ? tahunAwal : tahunAwal + '-' + tahunAkhir} `;
        let isDisplay = `${pengajuan.status == 'diterima' ? 'none' : pengajuan.status == 'ditolak' ? 'none' : ''}`;
        console.log(isDisplay);
        let cardHtml = `
                <div class="col-12 col-md-4 d-flex py-1" id="card-container">
                  <div class="col">
                    <div class="item-person d-flex">
                      <div class="item-person-cuti">
                        <div class="name-person-cuti mt-4 text-end">
                          <span>${pengajuan.nama}</span>
                        </div>
                        <div class="img-person-cuti">
                          <img src="../${pengajuan.profile_img}" class="img-fluid" alt="" />
                        </div>
                      </div>

                      <div class="item-text-cuti mt-3">
                        <h5 class="text-center">Pengajuan Cuti</h5>
                        <div class="item-text-cuti">
                          <ion-icon class="item-text-item" name="calendar-clear-outline"></ion-icon>
                          <span class="item-text-item">Tanggal Cuti</span>
                          <p class="text-item-text">${tglCuti}</p>
                          <ion-icon name="reader-outline"></ion-icon>
                          <span class="item-text-item">Tindakan</span>
                          <p class="text-item-text" id="status-pengajuan">${pengajuan.status}</p>
                          <ion-icon name="reader-outline"></ion-icon>
                          <span class="item-text-item">Alasan Cuti</span>
                          <p class="text-item-text"><i>"${pengajuan.alasanCuti}"</i></p>
                        </div>
                      </div>

                      <div class="d-grid gap-1 d-flex justify-content-center mt-1 mb-2" id="button-div" >
                        <button class="btn-confirm-cuti me-md-2" type="button" onclick="handleButton('${pengajuan.nama}', 'diterima')" style="display: ${isDisplay};">Terima</button>
                        <button class="btn-cancel-cuti" type="button" onclick="handleButton('${pengajuan.nama}', 'ditolak')" style="display: ${isDisplay};">Tolak</button>
                      </div>
                    </div>
                  </div>
                </div>`;
        $('#card-container').append(cardHtml);
      });
    },
  });
});

const handleButton = (nama, action) => {
  if (confirm(`Apakah yakin pengajuan ini mau ${action}?`)) {
    $.ajax({
      type: 'POST',
      url: '/api/v1/persetujuan_cuti',
      data: {
        nama,
        action,
      },
      success: function (res) {
        $('#button-div').hide();
        alert(res.msg);
        location.reload();
      },
    });
  }
};

// handle logout
const handleLogout = () => {
  if (confirm('Yakin mau logout, a?')) {
    $.removeCookie('token', null, { path: '/super_admin' });
    window.location.href = '/admin/login';
  }
};
