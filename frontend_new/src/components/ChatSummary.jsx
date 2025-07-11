import React, { useEffect, useState } from "react";
import "./chatSummary.css";

const ChatSummary = ({ response, userPrompt, onFollowUpClick }) => {
  const [showBotResponse, setShowBotResponse] = useState(false);

  useEffect(() => {
    if (response) {
      setShowBotResponse(false);
      setTimeout(() => setShowBotResponse(true), 500); // Simulate typing
    }
  }, [response]);

  if (!response) return null;

  return (
    <div className="chat-summary-container">
      {/* User Message */}
      <div className="chat-message user-message">
        <span className="chat-bubble">{userPrompt}</span>
      </div>

      {/* Bot Typing Simulation */}
      {showBotResponse ? (
        <div className="chat-message bot-message">
          <span className="chat-bubble">{response.slm || "🤖 I couldn't find an answer."}</span>
        </div>
      ) : (
        <div className="chat-message bot-message">
          <span className="chat-bubble typing-indicator">...</span>
        </div>
      )}

      {/* Follow-Up Suggestions */}
      {response.next && response.next.length > 0 && (
        <div className="chat-message bot-message followup-section">
          <div className="followup-label">💡 You can also ask:</div>
          <div className="followup-suggestions">
            {response.next.map((item, idx) => (
              <button
                key={idx}
                className="followup-chip"
                onClick={() => onFollowUpClick(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Maximize Prompt */}
      <div className="chat-message bot-message maximize-hint">
        📊 For full charts and visualizations, please maximize the dashboard ↗
      </div>
    </div>
  );
};

export default ChatSummary;
