let LoginPassword = false;

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