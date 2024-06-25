// event handler untuk menambahkan class is-selected
$(document).ready(function () {
  $('.card').click(function () {
    $('.card').removeClass('card-is-selected');
    $(this).addClass('card-is-selected');
    let hairStylistName = $('#hairStylistName').text().toLowerCase();
    console.log(hairStylistName);
    let hairStylistPrice = $('#hairStylistPrice').text();
    handleSelectedHairStylist([{ hairStylistName, hairStylistPrice }]);
  });
});

// function untuk memasukkan data id hairstylist ke localStorage
const handleSelectedHairStylist = (selectedHairStylist) => {
  let userData = JSON.parse(localStorage.getItem('userData'));
  console.log(userData);
  if (!userData) {
    alert('Data kamu gaada nih, silahkan isi data dirimu untuk booking ya~😉');
    return;
  }

  // update userData di LS
  localStorage.setItem('userData', JSON.stringify({ ...userData, selectedHairStylist }));
};
