function togglePassword(){

    const password =
    document.getElementById(
        "password"
    );

    const eyeIcon =
    document.getElementById(
        "eyeIcon"
    );

    if(password.type === "password"){

        password.type = "text";

        eyeIcon.className =
        "ti ti-eye-off";

    }else{

        password.type = "password";

        eyeIcon.className =
        "ti ti-eye";

    }
}