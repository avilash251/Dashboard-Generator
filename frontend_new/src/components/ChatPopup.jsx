import React, { useState } from 'react';
import SearchBar from './SearchBar';
import ChartContainer from './ChartContainer';
import './chatPopup.css';

const ChatPopup = ({ onClose, onMaximize }) => {
  const [chartData, setChartData] = useState([]);
  const [nextSuggestions, setNextSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearchSubmit = async (prompt) => {
    try {
      setIsLoading(true);
      const res = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      setChartData(data.layout || []);
      setNextSuggestions(data.next || []);
    } catch (err) {
      console.error("Error fetching charts:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-popup">
      <div className="chat-header">
        <span>🔍 Ask AI Dashboard</span>
        <div>
          <button onClick={onMaximize}>⛶</button>
          <button onClick={onClose}>✖</button>
        </div>
      </div>
      <div className="chat-body">
        <SearchBar onSearch={handleSearchSubmit} />
        {isLoading ? <p>Generating insights...</p> : null}
        <ChartContainer layout={chartData} next={nextSuggestions} />
      </div>
    </div>
  );
};

export default ChatPopup;
