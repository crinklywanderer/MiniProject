async function sendMessage() {
    const inputElement = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const input = inputElement.value.trim();

    if (!input) return;

    // Show user message
    chatbox.innerHTML += `<div><strong>You:</strong> ${input}</div>`;

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: input })  // 'message' should match what Flask expects
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Show bot response
        chatbox.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
    } catch (error) {
        console.error("Fetch error:", error);
        chatbox.innerHTML += `<div><strong>Bot:</strong> Oops! Something went wrong. Please try again later.</div>`;
    }

    inputElement.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;
}
