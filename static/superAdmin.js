const sidebarToggle = document.querySelector('#sidebar-toggle');
sidebarToggle.addEventListener('click', function () {
  document.querySelector('#sidebar').classList.toggle('collapsed');
});

$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_all_orders',
    data: {},
    success: function (res) {
      res.orders.map((order, index) => {
        let pendingStatus = 'bg-primary';
        let successStatus = 'bg-success';
        let cancelStatus = 'bg-warning';
        let date = order.tanggalBooking.split(' ')[0];
        let [day, month, year] = date.split('/');
        let bookingDate = new Date(`${year}-${month}-${day}`);
        let formattedBookingDate = bookingDate.toLocaleString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        let rowHtml = `<tr>
                        <th scope="row">${index + 1}</th>
                        <td>${order.name}</td>
                        <td>${formattedBookingDate}</td>
                        <td>${order.selectedServices.map((service) => service.serviceName)}</td>
                        <td>
                            <div class="${order.status == 'Cancel' ? cancelStatus : order.status == 'Pending' ? pendingStatus : successStatus} text-center rounded text-${order.status == 'Cancel' ? 'black' : 'white'} mx-3 w-auto">
                            ${order.status}</td>
                            </div>
                        </td>    
                      </tr>`;
        $('#table-body').append(rowHtml);
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
