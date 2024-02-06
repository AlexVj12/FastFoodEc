let all = document.querySelectorAll('.stars-inner');

let puntaje = document.querySelectorAll('.puntaje');

//console.log(all)
//console.log(puntaje)

const starTotal = 5;
for(var i = 0; i <all.length; i++){

   var numero = parseFloat(puntaje[i].innerHTML)
   const starPercentage = (numero / starTotal) * 100;
   const starPercentageRounded = `${(Math.round(starPercentage / 10) * 10)}%`;


   document.querySelectorAll(`.stars-inner`)[i].style.width = starPercentageRounded; 

}







