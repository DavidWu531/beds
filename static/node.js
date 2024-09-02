function show_password_login() {
    var password_type = document.getElementById("password");
    if (password_type.type === "password") {
    password_type.type = "text";
  } else {
    password_type.type = "password";
  }
}

function show_password_register() {
    var password_type = document.getElementById("password");
    var confirm_password_type = document.getElementById("confirm-password");
    if (password_type.type === "password") {
    password_type.type = "text";
  } else {
    password_type.type = "password";
  }

  if (confirm_password_type.type === "password") {
    confirm_password_type.type = "text";
  } else {
    confirm_password_type.type = "password"
  }
}