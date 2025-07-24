// frontend/main.js


// Global user info object
let userInfo = { name: "", age: "" };

// Show a welcome message on a page load
document.addEventListener("DOMContentLoaded", function () {
  appendMessage(" ", "bot");
});

// Handle form submission (user info input)
document.getElementById("user-form").addEventListener("submit", function (e) {
  e.preventDefault();
  userInfo.name = document.getElementById("user-name").value.trim() || "User";
  userInfo.age = document.getElementById("user-age").value.trim() || "Not provided";
  startChat();
});

// Skip button handler
document.getElementById("skip-button").addEventListener("click", function () {
  userInfo.name = "User";
  userInfo.age = "Not provided";
  startChat();
});

// Hide user info form, show chat UI
function startChat() {
  document.getElementById("user-form").style.display = "none";
  document.getElementById("chat-ui").style.display = "block";
  document.getElementById("input-area").style.display = "flex";
  appendMessage(`Assistant: Hello ${userInfo.name}, how can I help you today?`, "bot");
}

// Send chat message
async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(`${userInfo.name}: ${message}`, "user");
  input.value = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, name: userInfo.name, age: userInfo.age }),
    });

    const data = await response.json();
    appendMessage(`Assistant: ${data.response}`, "bot");
  } catch (error) {
    appendMessage("Assistant: Sorry, something went wrong.", "bot");
  }
}

// Append message with spacing and wrapper
function appendMessage(text, type) {
  const chatBox = document.getElementById("chat-box");
  const wrapper = document.createElement("div");
  wrapper.className = "chat-turn";

  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.textContent = text;

  wrapper.appendChild(msg);
  chatBox.appendChild(wrapper);

  // Add spacing between chat turns
  wrapper.style.marginBottom = "15px";

  chatBox.scrollTop = chatBox.scrollHeight;
}

// Theme Toggle
const toggleButton = document.getElementById('toggle-theme');
toggleButton.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  const isDark = document.body.classList.contains('dark-mode');
  toggleButton.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
});
