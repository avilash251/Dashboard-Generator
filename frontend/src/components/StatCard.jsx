import React from "react";
import "../styles/StatCard.css";

const StatCard = ({ title, value, source }) => {
  return (
    <div className="stat-card">
      <h4>
        {title} {source === "slm" && <span className="badge">🤖 SLM</span>}
        {source === "gemini" && <span className="badge">⚡ Gemini</span>}
      </h4>
      <p>{value}</p>
    </div>
  );
};

export default StatCard;
