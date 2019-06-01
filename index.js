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

function submitLocation() {
  var start = $('location_start').val();
  var destination = $('location_destination').val();
  $.ajax(databaseURL + 'destination', {
    headers: {
      'Authorization': 'Bearer ' + userIdToken,
      'Access-Control-Allow-Origin': '*'
    },
    method: 'POST',
    data: JSON.stringify({'start': start, 'destination': destination}),
    contentType : 'application/json'
  }).then(function(data){

  });
}