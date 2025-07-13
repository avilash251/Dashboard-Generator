import React, { useState } from "react";
import ChatSummary from "./ChatSummary";
import SearchBar from "./SearchBar";
import FollowUpList from "./FollowUpList";
import "./ChatPopup.css";

const ChatPopup = ({ onExpand }) => {
  const [summary, setSummary] = useState(null);
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);

  const handleMinimize = () => {
    setIsMinimized(true);
  };

  const handleMaximize = () => {
    setIsMinimized(false);
    onExpand();
  };

  const handleChatSubmit = async (prompt) => {
    setLoading(true);
    setSummary({ type: "info", message: "🤖 Thinking..." });

    try {
      const res = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();

      if (data.slm) {
        setSummary({ type: "slm", message: data.slm });
        setFollowUps(data.next || []);
      } else if (data.layout?.length > 0) {
        setSummary({
          type: "success",
          message: "Charts are ready. Click maximize to view full dashboard.",
        });
        setFollowUps(data.next || []);
      } else {
        setSummary({
          type: "info",
          message: "No data found. Try rephrasing your query.",
        });
      }
    } catch (err) {
      setSummary({ type: "error", message: "Error: " + err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-popup ${isMinimized ? "minimized" : ""}`}>
      <div className="chat-header">
        <span>🤖 Assistant</span>
        <div className="chat-controls">
          {isMinimized ? (
            <button className="maximize-btn" onClick={handleMaximize}>
              ⛶
            </button>
          ) : (
            <>
              <button className="minimize-btn" onClick={handleMinimize}>
                🗕
              </button>
              <button className="maximize-btn" onClick={handleMaximize}>
                ⛶
              </button>
            </>
          )}
        </div>
      </div>
      <div className="chat-body">
        <ChatSummary summary={summary} />
        {!isMinimized && (
          <FollowUpList suggestions={followUps} onSelect={handleChatSubmit} />
        )}
      </div>
      {!isMinimized && (
        <div className="chat-footer">
          <SearchBar
            placeholder="Ask a question..."
            onSearch={handleChatSubmit}
            loading={loading}
          />
        </div>
      )}
    </div>
  );
};

export default ChatPopup;
