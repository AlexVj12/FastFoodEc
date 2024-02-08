let counter = 1;
let imagen = document.getElementById("url-img-profile");
setInterval(function(){
  document.getElementById('radio' + counter).checked = true;
  counter++;
  if(counter>5){
    counter=1;
  }

},3500);

window.onload = function () {

  let logo = document.getElementById('img-profile-account');

  logo.onload = function () {
      
  };

  setTimeout(function(){
      cargarImagen()
  }, 1000);
};


// Initialize and add the map
function createMap(elementId, options) {
  return new google.maps.Map(document.getElementById(elementId), options);
}

function createMarker(map, position) {
  return new google.maps.Marker({
    position: position,
    map: map,
  });
}

function initMap() {
  // The location of Uluru
  const uluru = { lat: -2.6490671, lng: -81.6945067 };
  
  // The map, centered at Uluru
  const map = createMap("map", {
    zoom: 4,
    center: uluru,
  });
  
  createMarker(map, uluru);
}


  let all = document.querySelectorAll('.stars-inner');

  let puntaje = document.querySelectorAll('.puntaje');

  //console.log(all)
  //console.log(puntaje.innerHTML)

  const starTotal = 5;
  let  numero = parseFloat(puntaje[0].innerHTML)
  const starPercentage = (numero / starTotal) * 100;
  const starPercentageRounded = `${(Math.round(starPercentage / 10) * 10)}%`;
  document.querySelector(`.${all[0].className}`).style.width = starPercentageRounded; 
  


function cargarImagen(){
    let img = document.getElementById("img-profile-account");
    document.getElementById("img-profile-account").src= imagen.value;

    img.addEventListener('error', (event) => {
        swal("Error al cargar la imagen!", "Asegurese de que la url esta correcta\n Recuerde que la url debe terminar con \n .JPG O PNG!", "error");
        
    });

   
}

function pago(){
  setTimeout(pago, 5000);
  swal({
    title: "Pedido Realizado!",
    text: "Su pedido se ha procesado correctamente!",
    icon: "success",
    button: "Aceptar!",
  });
  
}

