import React from "react";
import "../styles/StatCard.css";

const StatCard = ({ title, value, color }) => (
  <div className="stat-card" style={{ backgroundColor: color }}>
    <h4>{title}</h4>
    <p>{value}</p>
  </div>
);

export default StatCard;
