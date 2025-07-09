import React, { useEffect, useState } from 'react';
import WidgetCard from './WidgetCard';
import FilterSidebar from './FilterSidebar';
import SearchBar from './SearchBar';
import '../styles/dashboard.css';
import '../styles/widget.css';
import { fetchLiveMetrics } from '../utils/websocket';

const Dashboard = () => {
  const [widgets, setWidgets] = useState([]);
  const [filteredWidgetIds, setFilteredWidgetIds] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearchSubmit = async (prompt) => {
    try {
      setLoading(true);
      const res = await fetch('http://localhost:8080/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();

      if (data.layout && data.layout.length > 0) {
        setWidgets(data.layout);
        setFilteredWidgetIds(data.layout.map((w) => w.id));
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleWidget = (widgetId) => {
    setFilteredWidgetIds((prev) =>
      prev.includes(widgetId)
        ? prev.filter((id) => id !== widgetId)
        : [...prev, widgetId]
    );
  };

  useEffect(() => {
    fetchLiveMetrics((liveUpdates) => {
      setWidgets((prevWidgets) =>
        prevWidgets.map((widget) => ({
          ...widget,
          value: liveUpdates[widget.id] || widget.value
        }))
      );
    });
  }, []);

  return (
    <div className="dashboard-container">
      <SearchBar onSearch={handleSearchSubmit} />
      <div className="dashboard-body">
        <FilterSidebar
          availableWidgets={widgets}
          selectedWidgets={filteredWidgetIds}
          onToggle={handleToggleWidget}
        />
        <div className="widget-grid">
          {loading ? (
            <div className="loading-indicator">Loading...</div>
          ) : (
            widgets
              .filter((widget) => filteredWidgetIds.includes(widget.id))
              .map((widget, idx) => <WidgetCard key={idx} data={widget} />)
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
