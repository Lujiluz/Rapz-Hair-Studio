$(document).ready(function () {
  //specifying the dates that cannot be booked
  const startDate = new Date('2024-06-20');
  const dates = [];

  for (let i = 0; i < 20; i++) {
    const currentDate = new Date(startDate);
    currentDate.setDate(startDate.getDate() + i);
    const formattedDate = `${currentDate.getMonth() + 1}/${currentDate.getDate()}/${currentDate.getFullYear()}`;
    dates.push(formattedDate);
  }
  //from here, you can just get booked dates from database, and make it as an array and pass it
  //to datesDisabled property

  $('#datepicker').datepicker({
    format: 'mm/dd/yyyy',
    todayHighlight: true,
    autoclose: true,
    datesDisabled: dates,
  });
});
