import React from "react";
import "../styles/TimeRangeSelector.css";

const RANGES = ["5m", "15m", "1h", "6h", "1d", "7d"];

const TimeRangeSelector = ({ value, onChange }) => {
  return (
    <div className="time-range-selector">
      <label>Time Range:</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {RANGES.map((range, i) => (
          <option key={i} value={range}>{range}</option>
        ))}
      </select>
    </div>
  );
};

export default TimeRangeSelector;
