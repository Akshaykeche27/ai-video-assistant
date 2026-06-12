const chatBox = document.getElementById("chat");

function addMessage(text, type) {
    const div = document.createElement("div");

    div.className = type;
    div.innerHTML = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    return div;
}

async function ask() {

    const input = document.getElementById("q");

    const question = input.value.trim();

    if (!question) {
        return;
    }

    addMessage(`<b>You:</b> ${question}, "user"`);

    input.value = "";

    const loader = addMessage(
        "<b>Bot:</b> Thinking...",
        "bot"
    );

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                video_id: videoId
            })
        });

        const data = await response.json();

        if (data.error) {
            loader.innerHTML = `<b>Error:</b> ${data.error}`;
            return;
        }

        loader.innerHTML = `<b>Bot:</b> ${data.answer}`;

    } catch (err) {

        loader.innerHTML =
            `<b>Error:</b> ${err.message}`;

        console.error(err);
    }
}