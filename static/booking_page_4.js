$(document).ready(function () {
  //nyoba buat bikin settingan supaya tanggal tertentu gabisa dipilih (ceritanya udah dibooking)
  const startDate = new Date('2024-06-20');
  const dates = [];

  for (let i = 0; i < 20; i++) {
    const currentDate = new Date(startDate);
    currentDate.setDate(startDate.getDate() + i);
    const formattedDate = `${currentDate.getMonth() + 1}/${currentDate.getDate()}/${currentDate.getFullYear()}`;
    dates.push(formattedDate);
  }

  $('#datepicker').datepicker({
    format: 'mm/dd/yyyy',
    todayHighlight: true,
    autoclose: true,
    datesDisabled: dates,
  });

  // handle tanggal dan waktu booking
  $('#next-btn').click(function () {
    // dapetin data tanggal
    let selectedDate = $('#datepicker').datepicker('getDate');
    if (!selectedDate) return alert('Tolong pilih tanggal datengmu, Kak!🙏');

    // dapetin data waktu
    let [hour, minute] = $('#time').val().split('.');
    if (!hour || !minute) return alert('Tolong pilih jam kedatanganmu, Kak!🙏');

    // satuin + format jadi ISOString
    let selectedDateAndTime = new Date(selectedDate);
    selectedDateAndTime.setHours(hour, minute);
    let formattedDateAndTime = selectedDateAndTime.toLocaleString('en-GB', { timeZone: 'Asia/Jakarta' }).replace(',', '');

    // simpan di LS
    let userData = JSON.parse(localStorage.getItem('userData'));
    if (!userData) {
      alert('Data kamu gaada nih, silahkan isi data dirimu untuk booking ya~😉');
      return;
    }
    userData.tanggalBooking = formattedDateAndTime;

    localStorage.setItem('userData', JSON.stringify(userData));

    try {
      $.ajax({
        type: 'POST',
        url: '/api/v1/addOrder',
        contentType: 'application/json',
        data: JSON.stringify(userData),
        success: function (res) {
          alert(res.msg);
          window.location.href = '/booking/5';
        },
      });
    } catch (e) {
      console.log(e);
    }
  });
});
