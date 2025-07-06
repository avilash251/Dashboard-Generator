import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";
import "../styles/DynamicChart.css";

const DynamicChart = ({ title, chartType = "line", data, thresholds = {}, pinned, onPin }) => {
  const hasData = data && data.length > 0;

  const exportCSV = () => {
    const rows = [["Time", "Value"], ...data.map(d => [d.time, d.value])];
    const csv = rows.map(r => r.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title.replace(/\s+/g, "_")}.csv`;
    a.click();
  };

  return (
    <div className={`dynamic-chart ${pinned ? "pinned" : ""}`}>
      <div className="chart-header">
        <h4>{title}</h4>
        <div className="chart-controls">
          <button onClick={exportCSV}>Export</button>
          <button onClick={() => onPin(title)}>{pinned ? "Unpin" : "📌 Pin"}</button>
        </div>
      </div>
      {!hasData ? (
        <p className="empty-message">⚠️ No data available.</p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="value"
              stroke={thresholds.warning && data.some(d => d.value > thresholds.warning) ? "red" : "#007bff"}
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default DynamicChart;
