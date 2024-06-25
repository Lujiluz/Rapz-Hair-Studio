const sidebarToggle = document.querySelector('#sidebar-toggle');
sidebarToggle.addEventListener('click', function () {
  document.querySelector('#sidebar').classList.toggle('collapsed');
});

$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_order_by_admin?hairStylistName=ntuy',
    success: function (res) {
      if (res.orders.length > 0) {
        res.orders.map((order) => {
          $('.random-text').hide();
          let cardHtml = `
                    <div class="col-12 col-md-4 d-flex py-1">
                      <div class="col">
                        <div class="item-person d-flex justify-content-center align-items-center mt-3">
                          <div class="item-identity-1">
                            <div class="name">
                              ${order.name}
                              <span><ion-icon name="person"></ion-icon></span>
                            </div>
                            <div class="number">
                              ${order.waNum}
                              <span><ion-icon name="call"></ion-icon></span>
                            </div>
                            <div class="email">
                              ${order.email}
                              <span><ion-icon name="mail"></ion-icon></span>
                            </div>
                          </div>
                          <div class="item-identity-2 mt-2">
                            <table class="d-flex justify-content-center align-items-center">
                              <tr>
                                <td>Service</td>
                                <td>:</td>
                                <td>${order.selectedServices.map((selectedService) => selectedService.serviceName)}</td>
                              </tr>
                              <tr>
                                <td>Date</td>
                                <td>:</td>
                                <td>${order.tanggalBooking.split(' ')[0]}</td>
                              </tr>
                              <tr>
                                <td>Time</td>
                                <td>:</td>
                                <td>${order.tanggalBooking.split(' ')[1]}</td>
                              </tr>
                              <tr>
                                <td>Status</td>
                                <td>:</td>
                                <td id='status-${order.userId}'>${order.status}</td>
                              </tr>
                            </table>
                          </div>
                          <div class="d-grid gap-2 d-flex justify-content-center mt-1">
                            <button class="btn-confirm" type="button" onclick="handleButton('Done', '${order.userId}')">Confirm</button>
                            <button class="btn-cancel" type="button" onclick="handleButton('Cancel', '${order.userId}')">Cancel</button>
                          </div>
                        </div>
                      </div>
                    </div>`;
          $('#card-container').append(cardHtml);
        });
      }
    },
  });
});

const handleButton = (status, userId) => {
  $(`#status-${userId}`).text(status);
  $.ajax({
    type: 'POST',
    url: `/api/v1/order_${status.toLowerCase()}`,
    data: { userId },
    success: function (res) {
      alert(res.msg);
      location.reload();
    },
  });
};
