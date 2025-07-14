import React, { useState } from "react";
import "../styles/ChatPopup.css";

function ChatPopup({ isOpen, onClose, onSubmit }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUserMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });

      const data = await res.json();
      const summaryText = data?.slm || (data.layout?.length
        ? "Charts and layout generated. Maximize to view."
        : "No charts found.");
      const assistantMsg = {
        role: "assistant",
        text: summaryText,
        followups: data?.next || [],
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", text: "⚠️ Error fetching response." }]);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  const handleFollowup = async (followupPrompt) => {
    setInput(followupPrompt);
    await handleUserMessage();
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleUserMessage();
  };

  return (
    <div className={`chat-popup ${isOpen ? "open" : ""}`}>
      <div className="chat-header">
        <span>🧠 Infra Assistant</span>
        <button onClick={onClose}>–</button>
      </div>
      <div className="chat-body">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-msg ${msg.role}`}>
            <div className="bubble">{msg.text}</div>
            {msg.followups && msg.followups.length > 0 && (
              <div className="followup-list">
                {msg.followups.map((f, i) => (
                  <button key={i} onClick={() => handleFollowup(f)} className="followup-btn">
                    {f}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="typing-indicator">AI is typing...</div>}
      </div>
      <div className="chat-footer">
        <input
          type="text"
          placeholder="Ask about your infrastructure..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button onClick={handleUserMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatPopup;
