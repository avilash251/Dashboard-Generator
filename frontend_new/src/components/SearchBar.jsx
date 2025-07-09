import React, { useState, useEffect, useRef } from 'react';
import '../styles/searchbar.css';

const suggestionsFallback = [
  "Show CPU usage for server1",
  "Disk I/O trend over last 6 hours",
  "HTTP 5xx error rate",
  "Memory usage for namespace kube-system",
  "Node latency P95 for cluster1"
];

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const ref = useRef();

  const handleSearch = () => {
    onSearch(query);
    setShowDropdown(false);
    setActiveIndex(-1);
  };

  const fetchSuggestions = async (input) => {
    if (input.length < 3) return;
    try {
      const res = await fetch(`http://localhost:8080/api/suggestion?q=${input}`);
      const data = await res.json();
      setSuggestions(data?.suggestions || []);
      setShowDropdown(true);
    } catch {
      setSuggestions(suggestionsFallback);
      setShowDropdown(true);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      setActiveIndex(prev => (prev + 1) % suggestions.length);
    } else if (e.key === 'ArrowUp') {
      setActiveIndex(prev => (prev - 1 + suggestions.length) % suggestions.length);
    } else if (e.key === 'Enter') {
      if (activeIndex >= 0) {
        setQuery(suggestions[activeIndex]);
        handleSearch();
      } else {
        handleSearch();
      }
    }
  };

  useEffect(() => {
    const handler = (e) => {
      if (!ref.current?.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="searchbar-container" ref={ref}>
      <div className="search-input-wrapper">
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            fetchSuggestions(e.target.value);
          }}
          onKeyDown={handleKeyDown}
        />
        <button className="search-btn" onClick={handleSearch}>🔍</button>
        <span className="brain-icon" onClick={() => setShowDropdown(!showDropdown)}>🧠</span>
      </div>
      {showDropdown && (
        <ul className="suggestions-dropdown">
          {suggestions.map((s, idx) => (
            <li
              key={idx}
              className={idx === activeIndex ? 'active' : ''}
              onClick={() => {
                setQuery(s);
                handleSearch();
              }}
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
