function validateRegister(){

    var pass1 = document.forms["register_form"]["password"].value;
    var pass2 = document.forms["register_form"]["password2"].value;
    var mail = document.forms["register_form"]["email"].value

    if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))) {
        alert("Wrong email format");
        return false
    }
    if (pass1 != pass2) {
        alert("Passwords don't match each other");
        return false;
    }
}