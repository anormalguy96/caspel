console.log("script.js loaded");

const promptInput = document.getElementById("prompt");
const sendButton = document.getElementById("send-button");
const responseBox = document.getElementById("response");

console.log("promptInput:", promptInput);
console.log("sendButton:", sendButton);
console.log("responseBox:", responseBox);

sendButton.addEventListener("click", async () => {
    console.log("BUTTON CLICKED");

    const prompt = promptInput.value.trim();
    console.log("prompt:", prompt);

    if (!prompt) {
        responseBox.textContent = "Prompt daxil edin.";
        return;
    }

    responseBox.textContent = "Cavab hazırlanır...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: prompt
            })
        });

        console.log("status:", response.status);

        const data = await response.json();
        console.log("data:", data);

        if (!response.ok) {
            responseBox.textContent =
                data.detail || "Xəta baş verdi.";
            return;
        }

        responseBox.innerHTML = marked.parse(data.response);

    } catch (error) {
        console.error("FETCH ERROR:", error);
        responseBox.textContent =
            "Serverə qoşulmaq mümkün olmadı.";
    }
});