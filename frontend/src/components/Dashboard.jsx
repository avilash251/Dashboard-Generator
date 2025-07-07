import React, { useState, useEffect } from "react";
import axios from "axios";
import socket from "../utils/socket";
import SearchBar from "./SearchBar";
import StatCard from "./StatCard";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState([]);
  const [liveStatus, setLiveStatus] = useState("🔴 Offline");

  const handleSearchSubmit = async (prompt) => {
    try {
      setLoading(true);
      const res = await axios.post("/api/chat", { prompt });
      setMetrics(res.data.metrics || []);
    } catch (err) {
      console.error("Chat API error:", err);
    } finally {
      setLoading(false);
    }
  };

  // 🧠 Listen to socket events
  useEffect(() => {
    socket.on("connect", () => {
      setLiveStatus("🟢 Live");
    });

    socket.on("disconnect", () => {
      setLiveStatus("🔴 Offline");
    });

    socket.on("live-status", (data) => {
      setLiveStatus(data.status || "🟢 Live");
    });

    socket.on("metric-update", (data) => {
      setMetrics((prev) => {
        const updated = [...prev];
        const index = updated.findIndex((m) => m.title === data.metric);
        if (index !== -1) {
          updated[index].value = data.value;
        } else {
          updated.push({ title: data.metric, value: data.value });
        }
        return updated;
      });
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("live-status");
      socket.off("metric-update");
    };
  }, []);

  return (
    <div className="dashboard-container">
      <h3>🔍 Agentic AI Dashboard <span style={{
        float: "right",
        fontSize: "0.85rem", 
        padding: "2px 6px",
        backgroundColor: "#eee",
        borderRadius: "4px"
        }}>{liveStatus}</span>
      </h3>
      <SearchBar onSearch={handleSearchSubmit} />
      {loading && <p>🔄 Loading...</p>}
      <div className="metric-cards">
        {metrics.map((metric, idx) => (
          <StatCard key={idx} title={metric.title} value={metric.value} threshold={metric.threshold} />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
