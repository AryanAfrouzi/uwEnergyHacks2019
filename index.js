firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    //get id token
    user.getIdToken().then(function(idToken) {
      userIdToken = idToken;
    });

    // User is signed in.

    document.getElementById("user_div").style.display = "block";
    document.getElementById("login_div").style.display = "none";

    var user = firebase.auth().currentUser;

    if(user != null){

      var email_id = user.email;
      document.getElementById("user_para").innerHTML = "Welcome User : " + email_id;

    }

  } else {
    // No user is signed in.

    document.getElementById("user_div").style.display = "none";
    document.getElementById("login_div").style.display = "block";

  }
});

function login(){
  var userEmail = document.getElementById("email_field").value;
  var userPass = document.getElementById("password_field").value;

  firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;

    window.alert("Error : " + errorMessage);

    // ...
  });

}

function logout(){
  firebase.auth().signOut();
}

$(document).on('click', ".car-type", function () {
  $('.selected-car').removeClass('active');
  $('.selected-car').removeClass('selected-car');
  $(this).addClass('active');
  $(this).addClass('selected-car');
});

var backendhosturl = 'https://green-route-api.appspot.com/api'
//create map using javascript api
function initMap() {
  //if data is submitted
  document.getElementById("submit").addEventListener("click", function(){
    var start = $('.location_start').val();
    var destination = $('.location_destination').val();
    var carModel = $('.selected-car').html();

    if(carModel == 'None') {
      alert("No Car Selected");
    }
    else {
      $.ajax(backendhosturl, {
        headers: {
          'Authorization': 'Bearer ' + userIdToken,
          'Access-Control-Allow-Origin': '*'
        },
        method: 'POST',
        data: JSON.stringify({'location1': start, 'location2': destination, 'cartype': carModel}),
        contentType : 'application/json'
      }).then(function(recieved) {
        data = recieved['path'];

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 7,
          center: {lat:data[Math.floor((data.length)/2)][0], lng: data[Math.floor((data.length)/2)][1]}
        })
      
        var startMarker = new google.maps.Marker({
          position: {lat:data[0][0], lng: data[0][1]},
          map: map,
          title: 'Start',
          label: 'S',
          animation: google.maps.Animation.DROP
        });

        var endMarker = new google.maps.Marker({
          position: {lat:data[data.length-1][0], lng: data[data.length-1][1]},
          map: map,
          title: 'End',
          label: 'E',
          animation: google.maps.Animation.DROP
        });
      
        var poly = new google.maps.Polyline({
          map: map,
          path: [],
          geodesic: true,
          strokeColor: '#00FF00',
          strokeOpacity: 1.0,
          strokeWeight: 2
        })

        var route = [];
        for(i=0; i < data.length; i++) {
          route.push({lat: data[i][0], lng: data[i][1]});
        }
        var path = poly.getPath();
        path = [];
        path = route;
        // update the polyline with the updated path
        poly.setPath(path); 
        //scrolls down to map
        document.getElementById('map').style.height = "500px";

        $('html, body').animate({
          scrollTop: $("#map").offset().top
        }, 1000);

        retrieveStats();
      }); 
    } 
  });
} 

var stats;

function retrieveStats() {
  $.ajax(backendhosturl, {
    headers: {
      'Authorization': 'Bearer ' + userIdToken,
    },
  }).then(function(data) {
    stats = data;
    console.log(stats);
  });
}
//populate stats for cars
document.getElementById("car1").addEventListener("click", function(){
  openTopNav();
  $('.activeCar').removeClass('activeCar');
  $('#car1').addClass('activeCar');

  $('.total-carbon').html(stats[0][0]);
  $('.average-carbon').html(stats[0][1]);
  $('.total-carbon-saved').html(stats[0][3]);
  $('.average-carbon-saved').html(stats[0][4]);
  $('.average-mpg').html(stats[0][6]);
  $('.total-miles-driven').html(stats[0][8]);
  $('.average-miles-driven').html(stats[0][9]);
  $('.average-speed').html(stats[0][11]);
});

document.getElementById("car2").addEventListener("click", function(){
  openTopNav();
  $('.activeCar').removeClass('activeCar');
  $('#car2').addClass('activeCar');

  $('.total-carbon').html(stats[1][0]);
  $('.average-carbon').html(stats[1][1]);
  $('.total-carbon-saved').html(stats[1][3]);
  $('.average-carbon-saved').html(stats[1][4]);
  $('.average-mpg').html(stats[1][6]);
  $('.total-miles-driven').html(stats[1][8]);
  $('.average-miles-driven').html(stats[1][9]);
  $('.average-speed').html(stats[1][11]);
});

document.getElementById("car3").addEventListener("click", function(){
  openTopNav();
  $('.activeCar').removeClass('activeCar');
  $('#car3').addClass('activeCar');

  $('.total-carbon').html(stats[2][0]);
  $('.average-carbon').html(stats[2][1]);
  $('.total-carbon-saved').html(stats[2][3]);
  $('.average-carbon-saved').html(stats[2][4]);
  $('.average-mpg').html(stats[2][6]);
  $('.total-miles-driven').html(stats[2][8]);
  $('.average-miles-driven').html(stats[2][9]);
  $('.average-speed').html(stats[2][11]);
});

document.getElementById("car4").addEventListener("click", function(){
  openTopNav();
  $('.activeCar').removeClass('activeCar');
  $('#car4').addClass('activeCar');

  $('.total-carbon').html(stats[3][0]);
  $('.average-carbon').html(stats[3][1]);
  $('.total-carbon-saved').html(stats[3][3]);
  $('.average-carbon-saved').html(stats[3][4]);
  $('.average-mpg').html(stats[3][6]);
  $('.total-miles-driven').html(stats[3][8]);
  $('.average-miles-driven').html(stats[3][9]);
  $('.average-speed').html(stats[3][11]);
});


//Maps autocomplete api
function initializeAutocomplete() {
  var startInput = document.getElementById('start');
  startAuto = new google.maps.places.Autocomplete(startInput);
  var endInput = document.getElementById('end');
  endAuto = new google.maps.places.Autocomplete(endInput);
}

initMap();
initializeAutocomplete();

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "275px";
  document.getElementById("main").style.marginLeft = "275px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
} 

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openTopNav() {
  document.getElementById("topsidenav").style.height = "500px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeTopNav() {
  document.getElementById("topsidenav").style.height = "0";
} 





