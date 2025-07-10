import React, { useState } from 'react';
import './dashboard.css';
import SearchBar from './SearchBar';
import WidgetCard from './WidgetCard';
import FilterSidebar from './FilterSidebar';

const Dashboard = () => {
  const [widgets, setWidgets] = useState([]);
  const [filteredCategories, setFilteredCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchPrompt, setSearchPrompt] = useState('');
  const [error, setError] = useState(null);

  const handleSearchSubmit = async (prompt) => {
    setLoading(true);
    setSearchPrompt(prompt);
    try {
      const res = await fetch('http://localhost:8080/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (data.layout) {
        setWidgets(data.layout);
      } else {
        setWidgets([]);
      }
    } catch (err) {
      console.error('API error:', err);
      setError('Failed to load dashboard widgets.');
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryToggle = (category, checked) => {
    setFilteredCategories((prev) =>
      checked ? [...prev, category] : prev.filter((c) => c !== category)
    );
  };

  const visibleWidgets = widgets.filter((w) =>
    filteredCategories.length === 0 ? true : filteredCategories.includes(w.category)
  );

  return (
    <div className="main-dashboard">
      <div className="dashboard-header">
        <SearchBar onSearch={handleSearchSubmit} />
      </div>

      <div className="dashboard-body">
        <div className="sidebar-section">
          <FilterSidebar widgets={widgets} onToggle={handleCategoryToggle} />
        </div>

        <div className="content-area">
          {loading ? (
            <div className="dashboard-loading">Loading...</div>
          ) : error ? (
            <div className="dashboard-error">{error}</div>
          ) : visibleWidgets.length > 0 ? (
            <div className="widget-container">
              {visibleWidgets.map((widget, idx) => (
                <WidgetCard key={idx} data={widget} />
              ))}
            </div>
          ) : (
            <div className="dashboard-empty">No widgets to display.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
