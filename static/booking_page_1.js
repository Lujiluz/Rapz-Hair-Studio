$(document).ready(function () {
  // =================BOOKING_PAGE_1==============================

  // function untuk generate userId
  const getUserId = () => {
    let id = localStorage.getItem('userId');
    if (!id) {
      id = 'user_' + new Date().getTime();
      localStorage.setItem('userId', id);
    }
    return id;
  };

  let userId = getUserId();
  // function untuk save data ke LS
  const saveUserData = () => {
    let userData = {
      userId,
      name: $('#name').val(),
      waNum: $('#waNum').val(),
      email: $('#email').val(),
    };
    localStorage.setItem('userData', JSON.stringify(userData));
  };

  // function untuk mengambil data user di LS
  const loadUserData = () => {
    let userData = JSON.parse(localStorage.getItem(userId));
    if (userData) {
      $('#name').val(userData.name);
      $('#waNum').val(userData.waNum);
      $('#email').val(userData.email);
    }
  };
  // memuat seluruh data user jika ada di LS
  loadUserData();
  // event listener untuk add data user ke localStorage
  $('.btn-next').click(function () {
    saveUserData();
    window.location.href = '/booking/2';
  });
});
