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
  const handleSearchSubmit = async (prompt) => {
  setLoading(true);
  setError(null);
  setChatSummary({
    type: "info",
    message: "Thinking... please wait.",
  });

  try {
    const res = await fetch(`${apiBase}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    if (data.error) throw new Error(data.error);

    const { slm, layout, next } = data;

    if (slm) {
      setChatSummary({ type: "slm", message: slm });
    } else if (layout?.length > 0) {
      setWidgetData(layout); // Render charts
      setChatSummary({
        type: "success",
        message: `Generated ${layout.length} PromQL charts. To view them, please maximize the dashboard.`,
      });
    } else {
      setChatSummary({
        type: "info",
        message: "No chart layout found. Try a different query or adjust filters.",
      });
    }

    setFollowUps(next || []);
  } catch (err) {
    setError(err.message);
    toast.error(`❌ ${err.message}`);
    setChatSummary({
      type: "error",
      message: `Something went wrong: ${err.message}`,
    });
  } finally {
    setLoading(false);
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
