import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "../styles/SearchBar.css";

const defaultSuggestions = [
  "Show CPU usage for server1",
  "Disk I/O trend over last 6 hours",
  "HTTP 5xx error rate",
  "Memory usage for namespace kube-system",
  "Node latency P95 for cluster1",
];

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef();

  const fetchSuggestions = async (input) => {
    try {
      if (input.length < 3) return setSuggestions([]);
      const res = await axios.get(`/api/suggestion?q=${input}`);
      setSuggestions(res.data || []);
    } catch (err) {
      console.error("❌ Failed to fetch suggestions:", err);
    }
  };

  const handleSearch = (prompt) => {
    if (!prompt.trim()) return;
    onSearch(prompt);
    setQuery("");
    setSuggestions([]);
    setActiveIndex(-1);
    setShowDropdown(false);

    // Save to history
    const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    const updated = [prompt, ...history.filter((h) => h !== prompt)].slice(0, 5);
    localStorage.setItem("searchHistory", JSON.stringify(updated));
  };

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setActiveIndex((prev) => (prev + 1) % suggestions.length);
    } else if (e.key === "ArrowUp") {
      setActiveIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length);
    } else if (e.key === "Enter") {
      if (activeIndex >= 0 && suggestions[activeIndex]) {
        handleSearch(suggestions[activeIndex]);
      } else {
        handleSearch(query);
      }
    }
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setQuery(val);
    fetchSuggestions(val);
    setShowDropdown(true);
  };

  const handleBrainClick = () => {
    setSuggestions(defaultSuggestions);
    setShowDropdown(true);
    inputRef.current.focus();
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(".searchbar-container")) {
        setShowDropdown(false);
        setActiveIndex(-1);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="searchbar-container">
      <div className="search-input-wrapper">
        <input
          ref={inputRef}
          type="text"
          placeholder="Ask your infrastructure question..."
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowDropdown(true)}
        />
        <span className="brain-icon-inside" onClick={handleBrainClick} title="Show suggestions">🧠</span>
        <button onClick={() => handleSearch(query)}>Search</button>
      </div>

      {showDropdown && suggestions.length > 0 && (
        <ul className="suggestion-dropdown">
          {suggestions.map((sug, idx) => (
            <li
              key={idx}
              className={idx === activeIndex ? "active" : ""}
              onClick={() => handleSearch(sug)}
            >
              {sug}
            </li>
          ))}
        </ul>
      )}
    </div>

  );
}

export default SearchBar;
