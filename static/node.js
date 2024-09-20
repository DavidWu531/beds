function show_password() {
    var password_type = document.getElementById("password");
    const icon_login = document.getElementById('password-login-eye-icon');
    if (password_type.type === "password") {
    password_type.type = "text";
    icon_login.classList.remove('fa-eye');
    icon_login.classList.add('fa-eye-slash');
  } else {
    password_type.type = "password";
    icon_login.classList.remove('fa-eye-slash');
    icon_login.classList.add('fa-eye');
  }
}


function show_password_password() {
  var password_type = document.getElementById("password");
  const icon_register = document.getElementById('password-eye-icon');
  if (password_type.type === "password") {
  password_type.type = "text";
  icon_register.classList.remove('fa-eye');
  icon_register.classList.add('fa-eye-slash');
} else {
  password_type.type = "password";
  icon_register.classList.remove('fa-eye-slash');
  icon_register.classList.add('fa-eye');
}
}


function show_password_confirm() {
  var confirm_password_type = document.getElementById("confirm-password");
  const icon = document.getElementById('confirm-eye-icon');
  if (confirm_password_type.type === "password") {
    confirm_password_type.type = "text";
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    confirm_password_type.type = "password"
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}