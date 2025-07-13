import React, { useState, useEffect, useRef } from "react";
import "./ChatPopup.css";
import { useNavigate } from "react-router-dom";
import { FaRobot, FaArrowUp, FaTimes, FaExpand } from "react-icons/fa";

const ChatPopup = ({ isOpen, setIsOpen }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input })
      });

      const data = await res.json();

      const aiSummary = data.slm || "Here is a summary of your request.";
      const followupNote =
        data.layout?.length > 0
          ? "📈 For full details and charts, please click Maximize to open the Prometheus Dashboard."
          : "🤖 No charts available for this query.";

      const assistantMessage = {
        role: "assistant",
        content: `${aiSummary}\n\n${followupNote}`
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Error fetching response." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  const handleMaximize = () => {
    setIsOpen(false);
    navigate("/promethus-dashboard");
  };

  const handleClose = () => {
    setIsOpen(false);
    navigate("/");
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  if (!isOpen) return null;

  return (
    <div className="chat-popup-container">
      <div className="chat-popup-header">
        <FaRobot className="robot-icon" />
        <span>AI Assistant</span>
        <div className="chat-popup-actions">
          <FaExpand onClick={handleMaximize} title="Maximize" />
          <FaTimes onClick={handleClose} title="Close" />
        </div>
      </div>

      <div className="chat-popup-body">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.role === "user" ? "user" : "bot"}`}
          >
            {msg.content}
          </div>
        ))}
        {isLoading && <div className="chat-bubble bot">Typing...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-popup-footer">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={handleSubmit}>
          <FaArrowUp />
        </button>
      </div>
    </div>
  );
};

export default ChatPopup;
