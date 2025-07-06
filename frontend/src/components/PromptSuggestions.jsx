import React from "react";
import "../styles/PromptSuggestions.css";

const examples = [
  "Show CPU usage for server1",
  "Disk I/O trend over last 6 hours",
  "HTTP 5xx error rate",
  "Memory usage for namespace kube-system",
  "Node latency P95 for cluster1"
];

const PromptSuggestions = ({ onPrompt }) => (
  <div className="suggestion-bar">
    <p>🧠 Try one of these:</p>
    <ul>
      {examples.map((prompt, index) => (
        <li key={index} onClick={() => onPrompt(prompt)}>{prompt}</li>
      ))}
    </ul>
  </div>
);

export default PromptSuggestions;
