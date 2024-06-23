$(document).ready(async function () {
  // =================BOOKING_PAGE_1==============================

  // function untuk hashing id
  const hashId = async (userId) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(userId);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  };
  // function untuk generate userId
  const getUserId = async () => {
    let id = localStorage.getItem('userId');
    if (!id) {
      id = 'user_' + new Date().getTime();
      hashedId = await hashId(id);
      localStorage.setItem('userId', hashedId);
    }
    return id;
  };

  let userId = await getUserId();
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
