import React from "react";
import "./chatSummary.css";

const ChatSummary = ({ response, userPrompt, onFollowUpClick }) => {
  if (!response) return null;

  return (
    <div className="chat-summary-container">
      {/* User Message */}
      <div className="chat-message user-message">
        <span className="chat-bubble">{userPrompt}</span>
      </div>

      {/* Bot Reply */}
      <div className="chat-message bot-message">
        <span className="chat-bubble">{response.slm || "🤖 I couldn't find an answer."}</span>
      </div>

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
