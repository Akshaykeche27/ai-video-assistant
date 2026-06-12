let currentTranscript = null;

const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggleBtn");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const closeSidebarBtn = document.getElementById("closeSidebarBtn");
const overlay = document.getElementById("overlay");
const sendBtn = document.getElementById("sendBtn");

if(toggleBtn){

toggleBtn.addEventListener("click",()=>{

    if(window.innerWidth > 768){
        sidebar.classList.toggle("collapsed");
    }
});

}

if(mobileMenuBtn){

mobileMenuBtn.addEventListener("click",()=>{

    sidebar.classList.add("mobile-open");
    overlay.classList.add("show");
    mobileMenuBtn.classList.add("hidden");
});

}

if(closeSidebarBtn){

closeSidebarBtn.addEventListener("click",()=>{

    sidebar.classList.remove("mobile-open");
    overlay.classList.remove("show");
    mobileMenuBtn.classList.remove("hidden");
});

}

if(overlay){

overlay.addEventListener("click",()=>{

    sidebar.classList.remove("mobile-open");
    overlay.classList.remove("show");
    mobileMenuBtn.classList.remove("hidden");
});

}

document.querySelectorAll(".view-btn").forEach(btn=>{

btn.addEventListener("click",()=>{

    currentTranscript = btn.dataset.transcript;

    fetch(`/history/view/${currentTranscript}`)
    .then(res=>res.json())
    .then(data=>{

        const chatBox =
        document.getElementById("chatBox");

        chatBox.innerHTML="";

        if (data.chats.length===0){
            chatBox.innerHTML=`
            <div class="Welcome-message>
            Start Asking questions About This transcript.</div>
            `;
            return;
        }

        data.chats.forEach(chat=>{

            chatBox.innerHTML += 
               ` <div class="user-message">
                    ${chat.question}
                </div>

                <div class="bot-message">
                    ${chat.answer}
                </div>
            `;
        });

        chatBox.scrollTop =
        chatBox.scrollHeight;
    });

    if(window.innerWidth <= 768){

        sidebar.classList.remove("mobile-open");
        overlay.classList.remove("show");
        mobileMenuBtn.classList.remove("hidden");
    }
});

});

sendBtn.addEventListener("click",sendMessage);

function sendMessage(){

    const input =
    document.getElementById("questionInput");

    const question =
    input.value.trim();

    if(!question){
        return;
    }

    if(!currentTranscript){
    showToast("Please select a transcript first.", "error");
    return;
}

    const chatBox =
    document.getElementById("chatBox");

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>`
    ;

    input.value = "";

    chatBox.innerHTML += 
       ` <div class="bot-message thinking-message" id="thinkingMessage">
            Thinking...
        </div>`
    ;

    chatBox.scrollTop =
    chatBox.scrollHeight;

    console.log("Transcript UUID:", currentTranscript);
    console.log("Question:", question);
    console.log(currentTranscript)
    fetch("/history/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            transcript_uuid: currentTranscript,
            question: question
        })
    })
    .then(res => {

        if(!res.ok){
            throw new Error(`
                HTTP Error ${res.status}
            `);
        }

        return res.json();
    })
    .then(data => {

        const loader =
        document.getElementById(
            "thinkingMessage"
        );

        if(loader){
            loader.remove();
        }

        chatBox.innerHTML += 
           ` <div class="bot-message">
                ${data.answer}
            </div>`
        ;

        chatBox.scrollTop =
        chatBox.scrollHeight;
    })
    .catch(error => {

        console.error(error);
        console.log(currentTranscript)
        const loader =
        document.getElementById(
            "thinkingMessage"
        );

        if(loader){
            loader.remove();
        }

        chatBox.innerHTML += `
            <div class="bot-message">
                Error loading response.
            </div>
       ` ;

        chatBox.scrollTop =
        chatBox.scrollHeight;
    });
}

document.getElementById("questionInput").addEventListener("keydown",(e)=>{
    if(e.key==="Enter"){
        sendMessage();
    }
});



function showToast(message, type = "success") {

    const toast = document.createElement("div");

    toast.className = `flash-message ${type}`;

    toast.innerHTML = `
        <div>
            <i class="ti ${
                type === "success"
                ? "ti-circle-check"
                : "ti-alert-circle"
            }"></i>
            ${message}
        </div>
    `;

    document
        .querySelector(".flash-container")
        .appendChild(toast);

    setTimeout(() => {
        toast.classList.add("flash-hide");

        setTimeout(() => {
            toast.remove();
        }, 400);

    }, 4000);
}