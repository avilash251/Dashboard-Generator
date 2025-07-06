import React, { useState } from "react";
import axios from "axios";
import SearchBar from "./SearchBar";
import StatCard from "./StatCard";
import DynamicChart from "./DynamicChart";
import MapView from "./MapView";
import PromptSuggestions from "./PromptSuggestions";
import EndpointSelector from "./EndpointSelector";
import TimeRangeSelector from "./TimeRangeSelector";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [query, setQuery] = useState("");
  const [charts, setCharts] = useState([]);
  const [stats, setStats] = useState({});
  const [categoryTabs, setCategoryTabs] = useState([]);
  const [activeTab, setActiveTab] = useState("all");
  const [timeRange, setTimeRange] = useState("1h");
  const [prometheusURL, setPrometheusURL] = useState("http://localhost:9090");
  const [pinnedCharts, setPinnedCharts] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (inputQuery) => {
    if (!inputQuery) return;
    setQuery(inputQuery);
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8080/api/chat", {
        prompt: inputQuery,
        time_range: timeRange,
        prometheus_url: prometheusURL,
      });

      const raw = response.data.response || "[]";
      let chartsFromGemini = [];
      try {
        chartsFromGemini = JSON.parse(raw);
      } catch (err) {
        console.warn("Fallback to static layout due to Gemini JSON error:", err);
        chartsFromGemini = [{
          category: "Error",
          title: "Gemini failed to respond",
          promql: "",
          chart_type: "text",
          thresholds: {},
          data: []
        }];
      }

      const promises = chartsFromGemini.map(async (chart) => {
        const series = await axios.post("http://localhost:8080/api/timeseries/query", {
          promql: chart.promql,
          prometheus_url: prometheusURL,
        });
        const values = series.data?.data?.result?.[0]?.values || [];
        const formatted = values.map(([ts, val]) => ({
          time: new Date(ts * 1000).toLocaleTimeString(),
          value: parseFloat(val),
        }));
        return { ...chart, data: formatted };
      });

      const resolved = await Promise.all(promises);
      setCharts(resolved);

      const uniqueCategories = [...new Set(resolved.map((c) => c.category || "misc"))];
      setCategoryTabs(["all", ...uniqueCategories]);

      const statsMap = {};
      resolved.forEach(chart => {
        if (chart.category && chart.data.length) {
          const lastVal = chart.data[chart.data.length - 1].value;
          statsMap[chart.category] = lastVal.toFixed(2);
        }
      });
      setStats(statsMap);
    } catch (err) {
      console.error("Failed to fetch charts:", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePin = (title) => {
    setPinnedCharts(
      pinnedCharts.includes(title)
        ? pinnedCharts.filter((t) => t !== title)
        : [...pinnedCharts, title]
    );
  };

  const visibleCharts = charts.filter(
    (c) => activeTab === "all" || c.category === activeTab
  );

  return (
    <div className="dashboard-container">
      <SearchBar onSearch={handleSearch} />
      {/* <div className="selectors">
        <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
        <EndpointSelector value={prometheusURL} onChange={setPrometheusURL} />
      </div> */}

      {loading && <p className="loading">⏳ Loading...</p>}

      {!loading && charts.length > 0 && (
        <>
          <div className="stat-row">
            {Object.entries(stats).map(([title, value]) => (
              <StatCard key={title} title={title} value={value} />
            ))}
          </div>
          {/* <MapView /> */}
          <div className="tabs">
            {categoryTabs.map((tab) => (
              <button
                key={tab}
                className={activeTab === tab ? "active-tab" : ""}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
          {visibleCharts.map((chart, i) => (
            <DynamicChart
              key={i}
              {...chart}
              pinned={pinnedCharts.includes(chart.title)}
              onPin={handlePin}
            />
          ))}
        </>
      )}
    </div>
  );
};

export default Dashboard;
