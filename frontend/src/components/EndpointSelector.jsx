import React from "react";
import "../styles/EndpointSelector.css";

const ENDPOINTS = [
  { name: "Localhost", url: "http://localhost:9090" },
  { name: "Demo Cluster", url: "https://prometheus.demo.do.prometheus.io" }
];

const EndpointSelector = ({ value, onChange }) => {
  return (
    <div className="endpoint-selector">
      <label>Prometheus:</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {ENDPOINTS.map((e, i) => (
          <option key={i} value={e.url}>{e.name}</option>
        ))}
      </select>
    </div>
  );
};

export default EndpointSelector;
