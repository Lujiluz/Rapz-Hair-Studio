// TODO: (booking_page_2) - memasukkan data services ke LS berdasarkan ID user dan memastikannya masuk dengan baik - DONE

$(document).ready(function () {
  // =================BOOKING_PAGE_2==============================
  $.ajax({
    type: 'GET',
    url: '/api/v1/get_services',
    data: {},
    success: function (res) {
      res.services.forEach((service) => {
        let temp = `
         <div class="col mb-2">
              <div class="card text-light position-relative" style="min-height: 115px">
                <div class="card-body px-4 pt-3 pb-5 shadow">
                  <div class="d-flex justify-content-between align-items-center">
                    <h5 class="card-title" id="service-title">${service.service_name}</h5>
                    <span class="text-light">
                      <h5 id="service-price">${service.price}</h5>
                    </span>
                  </div>
                  <p class="card-text" id="service-desc">${service.desc}</p>
                  <button class="service-button btn btn-sm position-absolute bottom-0 end-0 mt-2 mb-3 me-3" data-service-id="${service.service_id}" data-service-name="${service.service_name}" data-service-price="${service.price}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                      <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
        `;
        $('#card-container').append(temp);
      });
    },
  });
});

// handler function untuk memasukkan ID service ke LS
const handleServiceSelected = (serviceId, serviceName, price) => {
  let userData = JSON.parse(localStorage.getItem('userData'));
  if (!userData) {
    alert('Data kamu gaada nih, silahkan isi data dirimu untuk booking ya~😉');
    return;
  }

  // buat selectedServices kalo belum ada
  if (!userData.selectedServices) {
    userData.selectedServices = [];
  }

  //cek apakah serviceId udah ada atau belum. Kalau belum masukin, kalau ada keluarin
  const index = userData.selectedServices.findIndex((service) => service.serviceId == serviceId);
  if (index === -1) {
    let serviceDetail = {
      serviceId,
      price,
      serviceName,
    };
    userData.selectedServices.push(serviceDetail);
  } else {
    userData.selectedServices.splice(index, 1);
  }

  // update userData di LS
  localStorage.setItem('userData', JSON.stringify(userData));
  console.log(userData);
};

$('#card-container').on('click', '.service-button', function () {
  const serviceId = $(this).data('service-id');
  const serviceName = $(this).data('service-name');
  const servicePrice = $(this).data('service-price');
  handleServiceSelected(serviceId, serviceName, servicePrice);

  // update icon dari button berdasarkan state button
  let xIcon = ` <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                    <path d="M2.146 2.146a.5.5 0 0 1 .708 0L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854a.5.5 0 0 1 0-.708z" />
                  </svg>
    `;
  const plusIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                      <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2" />
                    </svg>`;
  let card = $(this).closest('.card');
  // mengubah opacity card ketika service dipilih
  card.toggleClass('card-selected');

  //   mengubah icon svg: jika service dipilih icon 'x', jika tidak icon '+'
  if (card.hasClass('card-selected')) {
    $(this).html(xIcon);
  } else {
    $(this).html(plusIcon);
  }
});
