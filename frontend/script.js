const chatbox = document.getElementById("chatbox");
const form = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const domainSelect = document.getElementById("domain");
const useDomainCheckbox = document.getElementById("use-domain");

let userId = null; // will store user_id from backend

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  const p = document.createElement("p");
  p.textContent = text;
  div.appendChild(p);
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = userInput.value.trim();
  if (!question) return;

  appendMessage(question, "user");
  userInput.value = "";

  try {
    const response = await fetch("http://localhost:8000/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        user_id: userId,
        domain: domainSelect.value,
        use_domain: useDomainCheckbox.checked,
      }),
    });

    const data = await response.json();
    userId = data.user_id; // save user id for session persistence
    appendMessage(data.response, "bot");
  } catch (err) {
    appendMessage("Error: Could not reach backend", "bot");
  }
});
