import React, { useState, useEffect } from "react";
import SearchBar from "./SearchBar";
import ChatSummary from "./ChatSummary";
import WidgetCard from "./WidgetCard";
import "./dashboard.css";
import sampleData from "../sample.json"; // fallback
import { fetchChartData } from "../api/prometheus";

const Dashboard = () => {
  const [userPrompt, setUserPrompt] = useState("");
  const [chatResponse, setChatResponse] = useState(null);
  const [widgetData, setWidgetData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // 🔁 When user submits prompt
  const handlePromptSubmit = async (prompt) => {
    setUserPrompt(prompt);
    setIsLoading(true);
    setChatResponse(null);
    setWidgetData([]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      setChatResponse(data);

      // 🎯 If layout (promql) is returned, fetch live values
      if (data.layout && Array.isArray(data.layout)) {
        const enriched = await Promise.all(
          data.layout.map(async (widget) => {
            const value = await fetchChartData(widget.promql);
            return { ...widget, value };
          })
        );
        setWidgetData(enriched);
      }
    } catch (err) {
      console.error("Prompt submit failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFollowUpClick = (followup) => {
    handlePromptSubmit(followup);
  };

  return (
    <div className="dashboard-wrapper">
      <SearchBar onSubmit={handlePromptSubmit} />
      <div className="main-content">
        <ChatSummary
          userPrompt={userPrompt}
          response={chatResponse}
          onFollowUpClick={handleFollowUpClick}
        />

        {isLoading && <p className="loading">🔄 Fetching data...</p>}

        <div className="widget-grid">
          {widgetData.map((widget, idx) => (
            <WidgetCard key={idx} data={widget} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
