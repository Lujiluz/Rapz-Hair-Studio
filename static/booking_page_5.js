$(document).ready(function () {
  let userData = JSON.parse(localStorage.getItem('userData'));
  let userId = userData.userId;

  $.ajax({
    type: 'GET',
    url: `/api/v1/get_orders/${userId}`,
    data: {},
    success: function (res) {
      console.log(res.order_data);
      // menampilkan data pemesan
      $('#name').text(res.order_data.name);
      $('#waNum').text(res.order_data.waNum);
      $('#email').text(res.order_data.email);
      let [date, time] = res.order_data.tanggalBooking.split(' ');
      let bookingDate = new Date(date);
      let formattedBookingDate = bookingDate.toLocaleString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
      let [hours, minutes] = time.split(':');
      let formattedBookingTime = `${hours}.${minutes} WIB`;
      $('#date').text(formattedBookingDate);
      $('#time').text(formattedBookingTime);

      // menampilkan data orderan
      res.order_data.services_order.forEach((service) => {
        let services_html = `<p>${service.serviceName} <span class="float-end">Rp. ${service.price.slice(0, -1)}.000</span></p>`;
        $('#services').append(services_html);
      });
      res.order_data.barber_order.forEach((barber) => {
        let barber_html = `<p>${barber.hairStylistName} <span class="float-end">Rp. ${barber.hairStylistPrice.slice(0, -1)}.000</span></p>`;
        $('#barbers').append(barber_html);
      });
      $('#totalPay').text(`Rp. ${res.order_data.total_pay}.000`);
    },
  });
});

const handleNextBtn = () => {
  return confirm('Apakah data pesananmu sudah benar?') ? (window.location.href = '/booking/6') : '/booking/5';
};
