function showForm(type){

    const videoForm =
    document.getElementById("videoForm");

    const meetingForm =
    document.getElementById("meetingForm");

    if(videoForm && meetingForm){

        videoForm.style.display = "none";
        meetingForm.style.display = "none";

        if(type === "video"){

            videoForm.style.display = "block";

        }else{

            meetingForm.style.display = "block";

        }
    }
}

function toggleMenu(){

    const nav =
    document.getElementById(
        "navContainer"
    );

    nav.classList.toggle(
        "active"
    );
}


setTimeout(() => {

    document
        .querySelectorAll(".flash-message")
        .forEach(msg => {

            msg.style.opacity = "0";

            setTimeout(() => {

                msg.remove();

            }, 400);

        });

}, 4000);


document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".flash-message");

    messages.forEach((msg) => {

        setTimeout(() => {
            msg.classList.add("flash-hide");

            setTimeout(() => {
                msg.remove();
            }, 400);

        }, 4000);

        msg.querySelector(".flash-close").addEventListener("click", () => {
            msg.classList.add("flash-hide");

            setTimeout(() => {
                msg.remove();
            }, 400);
        });
    });
});