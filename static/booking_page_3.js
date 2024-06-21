// event handler untuk menambahkan class is-selected
$(document).ready(function () {
  $('.card').click(function () {
    $('.card').removeClass('card-is-selected');
    $(this).addClass('card-is-selected');
    let hairStylistId = $(this).data('hairstylist-id');
    handleSelectedHairStylist(hairStylistId);
  });
});

// function untuk memasukkan data id hairstylist ke localStorage
const handleSelectedHairStylist = (hairStylistId) => {
  let userData = JSON.parse(localStorage.getItem('userData'));
  if (!userData) {
    alert('Data kamu gaada nih, silahkan isi data dirimu untuk booking ya~😉');
    return;
  }

  // update userData di LS
  localStorage.setItem('userData', JSON.stringify({ ...userData, hairStylistId }));
};
