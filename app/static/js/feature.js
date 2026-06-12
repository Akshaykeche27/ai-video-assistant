function showForm(type){

    const videoForm =
    document.getElementById("videoForm");

    const meetingForm =
    document.getElementById("meetingForm");

    videoForm.style.display = "none";
    meetingForm.style.display = "none";

    if(type === "video"){

        videoForm.style.display = "block";

    }else{

        meetingForm.style.display = "block";
    }
}