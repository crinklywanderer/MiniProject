// Display welcome message when the page loads
document.addEventListener('DOMContentLoaded', function() {
  appendMessage("Assistant: Welcome to the AI Cancer Assistant! How can I help you today?", "bot");
});

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(`You: ${message}`, "user");
  input.value = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    appendMessage(`Assistant: ${data.response}`, "bot");
  } catch (error) {
    appendMessage("Assistant: Sorry, something went wrong.", "bot");
  }
}

function appendMessage(text, type) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}
