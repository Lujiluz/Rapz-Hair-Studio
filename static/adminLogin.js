const handleLogin = (role) => {
  let username = $('#username').val();
  let password = $('#password').val();
  $.ajax({
    type: 'POST',
    url: '/api/v1/admin_login',
    contentType: 'application/json',
    data: JSON.stringify({
      role,
      username,
      password,
    }),
    success: function (res) {
      if (res.code == 200) {
        $.cookie('token', res.token, { path: `/${res.role}` });
        alert('Berhasil login, a!');
        window.location.href = `/${res.role}/dashboard`;
      } else if (res.code == 401) {
        console.log(res);
        alert(res.msg);
      } else {
        alert('Ada masalah di sistem, jadi belum bisa login, a. Harap hubungi developer-mu!');
      }
    },
  });
};
