let LoginPassword = false;
let SignupPassword = false;
let ConfirmPassword = false;

$("#hidebutton1").on("click", function(event) {
  if (LoginPassword){
    document.getElementById("LoginPassword").setAttribute("type","text");
    document.getElementById("hidebutton1").src = "static/view.png";
    LoginPassword = false;
  }else{
    document.getElementById("LoginPassword").setAttribute("type","password");
    document.getElementById("hidebutton1").src = "static/hidden.png";
    LoginPassword = true;
  }
});

$("#hidebutton2").on("click", function(event) {
  if (SignupPassword){
    document.getElementById("SignupPassword").setAttribute("type","text");
    document.getElementById("hidebutton2").src = "static/view.png";
    SignupPassword = false;
  }else{
    document.getElementById("SignupPassword").setAttribute("type","password");
    document.getElementById("hidebutton2").src = "static/hidden.png";
    SignupPassword = true;
  }
});

$("#hidebutton3").on("click", function(event) {
  if (ConfirmPassword){
    document.getElementById("ConfirmPassword").setAttribute("type","text");
    document.getElementById("hidebutton3").src = "static/view.png";
    ConfirmPassword = false;
  }else{
    document.getElementById("ConfirmPassword").setAttribute("type","password");
    document.getElementById("hidebutton3").src = "static/hidden.png";
    ConfirmPassword = true;
  }
});