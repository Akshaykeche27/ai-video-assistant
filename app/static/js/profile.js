function logoutUser(){

    const confirmLogout =
    confirm("Are you sure you want to logout?");

    if(confirmLogout){

        alert("Logout Successful");

        window.location.href = "/login";
    }
}