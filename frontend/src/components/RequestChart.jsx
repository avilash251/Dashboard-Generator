import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const sampleData = [
  { time: "09:00", value: 100 },
  { time: "09:30", value: 120 },
  { time: "10:00", value: 90 },
  { time: "10:30", value: 160 },
  { time: "11:00", value: 140 }
];

const RequestChart = () => (
  <div style={{ marginTop: "40px" }}>
    <h3>Request Statistics Over Time</h3>
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={sampleData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#007bff" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default RequestChart;
