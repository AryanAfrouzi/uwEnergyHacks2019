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
        console.log(recieved);
        data = recieved['path'];

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 9,
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
      }); 
    } 
  });
} 

//Maps autocomplete api
function initializeAutocomplete() {
  var startInput = document.getElementById('start');
  startAuto = new google.maps.places.Autocomplete(startInput);
  var endInput = document.getElementById('end');
  endAuto = new google.maps.places.Autocomplete(endInput);
}

initMap();
initializeAutocomplete();









