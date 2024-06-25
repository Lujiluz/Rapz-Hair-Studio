$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_testimoni',
    data: {},
    success: function (res) {
      res.testimoni.map((testi) => {
        let star = '⭐';
        let cardHtml = `<div class="col-12 col-md-4 d-flex py-1">
                  <div class="col">
                    <div class="item-testi">
                      <div class="card-text">
                        <div class="card-item-testi d-flex">
                          <div class="col-2">
                            <img src="../static/img/icon-kutip.svg" alt="" />
                          </div>
                          <div class="col-10">
                            <h4 class="text-talent">${testi.name}</h4>

                            <p class="stars">${star.repeat(testi.rating)}</p>

                            <h5 class="text-testi mt-2">${testi.review}</h5>
                          </div>
                        </div>
                        <div class="choice text-center mt-3">
                          <a href="#">
                            <ion-icon class="icon-testi add" name="add-circle"></ion-icon>
                          </a>
                          <span class="icon-testi">|</span>
                          <a href="#">
                            <ion-icon class="icon-testi trash" name="trash"></ion-icon>
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>`;
        $('#card-container').append(cardHtml);
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
