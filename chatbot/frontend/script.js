// script.js
const API_BASE = "http://127.0.0.1:8000";

let currentConversationId = null;
const convListEl = document.getElementById("conversations");
const chatWindow = document.getElementById("chat-window");
const newConvBtn = document.getElementById("new-conv");
const sendBtn = document.getElementById("send");
const msgInput = document.getElementById("message-input");
const domainSelect = document.getElementById("domain-select");
const useDomainCheckbox = document.getElementById("use-domain");

newConvBtn.addEventListener("click", createConversation);
sendBtn.addEventListener("click", sendMessage);
msgInput.addEventListener("keydown", (e) => { if (e.key === "Enter") sendMessage(); });

async function createConversation() {
  const res = await fetch(`${API_BASE}/start`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({title:"New Conversation"}) });
  const data = await res.json();
  currentConversationId = data.conversation_id;
  refreshConversations();
  chatWindow.innerHTML = "";
}

async function refreshConversations() {
  // Simple UX: show current conversation only (you can expand to list with DB query endpoint)
  convListEl.innerHTML = "";
  if (currentConversationId) {
    const div = document.createElement("div");
    div.className = "conv-item active";
    div.innerText = `Conversation #${currentConversationId}`;
    convListEl.appendChild(div);
  } else {
    convListEl.innerHTML = `<div class="conv-item">No conversation. Click + New Conversation</div>`;
  }
}

async function sendMessage() {
  const text = msgInput.value.trim();
  if (!text) return;
  if (!currentConversationId) {
    // auto-create conversation
    await createConversation();
  }

  // show user message
  appendMessage("user", text);
  msgInput.value = "";

  const payload = {
    conversation_id: currentConversationId,
    message: text,
    domain: domainSelect.value || null,
    use_domain: useDomainCheckbox.checked
  };

  // call backend
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();

  appendMessage("bot", data.response);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.innerText = text;
  chatWindow.appendChild(div);
}

// on load
refreshConversations();
