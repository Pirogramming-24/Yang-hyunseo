const form = document.getElementById("generate-form");
const chatContainer = document.getElementById("chat-container");

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerText = text;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

form.addEventListener("submit", async function(e) {
    e.preventDefault();
    const text = this.message.value.trim();
    if (!text) return;

    appendMessage(text, "user");
    this.message.value = "";

    const res = await fetch("/api/generate/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    appendMessage(data.reply || data.error, "ai");
});