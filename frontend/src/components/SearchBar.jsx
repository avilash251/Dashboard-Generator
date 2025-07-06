import React, { useEffect, useState } from "react";
import "../styles/SearchBar.css";

const STATIC_SUGGESTIONS = [
  "Show CPU usage for server1",
  "Disk I/O trend over last 6 hours",
  "HTTP 5xx error rate",
  "Memory usage for namespace kube-system",
  "Node latency P95 for cluster1"
];

const TIME_RANGES = ["5m", "15m", "1h", "6h", "12h", "24h"];

const SearchBar = ({ onSearch }) => {
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const [isStaticMode, setIsStaticMode] = useState(false);
  const [timeRange, setTimeRange] = useState("1h");
  const [promUrl, setPromUrl] = useState("http://localhost:9090");

  const fetchDynamicSuggestions = async () => {
    if (input.length < 3) return;
    try {
      const res = await fetch("http://localhost:8080/api/suggestions");
      const data = await res.json();
      const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
      const merged = [...new Set([...history, ...(data.suggestions || [])])];
      setSuggestions(merged);
    } catch (err) {
      console.error("Failed to load suggestions", err);
    }
  };

  useEffect(() => {
    fetchDynamicSuggestions();
  }, [input]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      if (highlightedIndex >= 0 && highlightedIndex < filteredSuggestions.length) {
        submitSearch(filteredSuggestions[highlightedIndex]);
      } else {
        submitSearch(input);
      }
    } else if (e.key === "ArrowDown") {
      setHighlightedIndex((prev) =>
        Math.min(prev + 1, filteredSuggestions.length - 1)
      );
    } else if (e.key === "ArrowUp") {
      setHighlightedIndex((prev) => Math.max(prev - 1, 0));
    }
  };

  const submitSearch = (query) => {
    if (!query) return;
    const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    const updatedHistory = [query, ...history.filter((q) => q !== query)].slice(0, 10);
    localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));
    onSearch(query, timeRange, promUrl);
    setShowSuggestions(false);
    setHighlightedIndex(-1);
  };

  const handleSelect = (s) => {
    setInput(s);
    submitSearch(s);
  };

  const handleBrainClick = () => {
    setIsStaticMode(true);
    setSuggestions(STATIC_SUGGESTIONS);
    setShowSuggestions(!showSuggestions);
  };

  const filteredSuggestions = (isStaticMode ? STATIC_SUGGESTIONS : suggestions).filter((s) =>
    s.toLowerCase().includes(input.toLowerCase())
  );

  return (
    <div className="search-bar-wrapper">
      {/* <div className="dropdowns">
        <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
          {TIME_RANGES.map((range) => (
            <option key={range} value={range}>{range}</option>
          ))}
        </select>
        <input
          type="text"
          value={promUrl}
          onChange={(e) => setPromUrl(e.target.value)}
          placeholder="Prometheus URL"
        />
      </div> */}

      <div className="input-wrapper">
        <span className="brain-icon" onClick={handleBrainClick}>🧠</span>
        <input
          type="text"
          id="search-input"
          placeholder="Ask me about server metrics..."
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            setHighlightedIndex(-1);
          }}
          onKeyDown={handleKeyPress}
          onClick={() => setShowSuggestions(true)}
        />
        <button onClick={() => submitSearch(input)}>Search</button>
      </div>

      {showSuggestions && filteredSuggestions.length > 0 && (
        <ul className="autocomplete-list">
          {filteredSuggestions.map((s, i) => (
            <li
              key={i}
              onClick={() => handleSelect(s)}
              className={highlightedIndex === i ? "highlighted" : ""}
            >
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
