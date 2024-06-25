$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_user',
    data: {},
    success: function (res) {
      res.users.map((user) => {
        if (user.role === 'admin') {
          let cardHtml = `<div class="col-12 col-md-4 d-flex py-1">
                  <div class="col">
                    <div class="item-person d-flex">
                      <div class="item-person-cuti">
                        <div class="name-person-cuti mt-4 text-end">
                          <span>${user.fullName}</span>
                        </div>
                        <div class="img-person-cuti">
                          <img src="../${user.profile_img}" class="img-fluid" alt="" />
                        </div>
                      </div>

                      <div class="item-text-cuti mt-3">
                        <div class="item-text-cuti">
                          <ion-icon name="person-outline"></ion-icon>
                          <span class="item-text-item">Nama</span>
                          <p class="text-item-text">${user.fullName}</p>
                          <hr />

                          <ion-icon name="mail-outline"></ion-icon>
                          <span class="item-text-item">Email</span>
                          <p class="text-item-text">${user.email}</p>
                          <hr />

                          <ion-icon name="logo-whatsapp"></ion-icon>
                          <span class="item-text-item">No.Whatsapp</span>
                          <p class="text-item-text">${user.wa_num}</p>
                          <hr />

                          <ion-icon name="shield-checkmark-outline"></ion-icon>
                          <span class="item-text-item">Status</span>
                          <p class="text-item-text">${user.status}</p>
                          <hr />

                          <ion-icon name="logo-usd"></ion-icon>
                          <span class="item-text-item">Service Price</span>
                          <p class="text-item-text">Rp.${user.price_per_service}.000</p>
                          <hr />
                        </div>
                      </div>

                      <div class="d-flex justfy-content-center align-items-center text-center"></div>

                      <div class="item-icon-testi text-center mt-1 mb-2">
                        <a href=""><ion-icon class="icon-user edit" name="pencil"></ion-icon></a>
                        <span class="icon-user">|</span>
                        <a class="icon-user delete" href=""><ion-icon name="trash"></ion-icon></a>
                      </div>
                    </div>
                  </div>
                </div>`;
          $('#card-container').append(cardHtml);
        }
      });
    },
  });
});

// handle logout
const handleLogout = () => {
  if (confirm('Yakin mau logout, a?')) {
    $.removeCookie('token', null, { path: '/super_admin' });
    window.location.href = '/admin/login';
  }
};
