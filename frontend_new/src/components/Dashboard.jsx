import React, { useState } from "react";
import SearchBar from "./SearchBar";
import RequestChart from "./RequestChart";
import WidgetCard from "./WidgetCard";
import "./Dashboard.css";

const Dashboard = () => {
  const [layoutData, setLayoutData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [widgets, setWidgets] = useState([]);
  const [error, setError] = useState(null);

  const handleSearchSubmit = async (query) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: query }),
      });

      const data = await response.json();

      if (data?.layout?.length) {
        setLayoutData(data.layout);
      } else {
        setLayoutData([]);
      }

      if (data?.widgets?.length) {
        setWidgets(data.widgets);
      }

    } catch (err) {
      setError("Failed to fetch data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Prometheus Dashboard Assistant</h2>
        <SearchBar onSubmit={handleSearchSubmit} />
      </div>

      {loading && <p className="loading">🔄 Fetching data...</p>}
      {error && <p className="error">{error}</p>}

      <div className="widget-section">
        {widgets.map((widget, idx) => (
          <WidgetCard key={idx} data={widget} />
        ))}
      </div>

      <div className="chart-section">
        {layoutData.map((chart, idx) => (
          <RequestChart key={idx} chartData={chart} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
