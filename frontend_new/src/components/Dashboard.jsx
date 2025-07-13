import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import SearchBar from './SearchBar';
import ChatSummary from './ChatSummary';
import RequestChart from './RequestChart';
import WidgetCard from './WidgetCard';
import FilterSidebar from './FilterSidebar';
import sampleLayout from '../data/sample.json';

const Dashboard = () => {
  const [prompt, setPrompt] = useState('');
  const [layout, setLayout] = useState([]);
  const [slmResponse, setSlmResponse] = useState('');
  const [followUp, setFollowUp] = useState([]);
  const [loading, setLoading] = useState(false);
  const [widgets, setWidgets] = useState([]);
  const [visibleWidgets, setVisibleWidgets] = useState({});

  // Toggle visibility by checkbox
  const toggleWidget = (title) => {
    setVisibleWidgets(prev => ({
      ...prev,
      [title]: !prev[title]
    }));
  };

  // Handle search submission
  const handleSearchSubmit = async (query) => {
    setPrompt(query);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8080/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query })
      });

      const data = await res.json();

      if (data.error) {
        console.error(data.error);
        setLayout([]);
        setWidgets([]);
      } else {
        setSlmResponse(data.slm || '');
        setLayout(data.layout || []);
        setFollowUp(data.next || []);
        setWidgets(data.layout || []);
        setVisibleWidgets(
          Object.fromEntries((data.layout || []).map(w => [w.title, true]))
        );

        // Auto-expand if in chat mode
        if (window.location.pathname !== "/prometheus-dashboard" && data.layout?.length > 0) {
          window.location.href = "/prometheus-dashboard";
        }
      }
    } catch (err) {
      console.error(err);
      setLayout([]);
      setWidgets([]);
    } finally {
      setLoading(false);
    }
  };

  // Fallback to sample layout (for demo or no API)
  useEffect(() => {
    if (layout.length === 0 && !loading) {
      setWidgets(sampleLayout);
      setVisibleWidgets(
        Object.fromEntries(sampleLayout.map(w => [w.title, true]))
      );
    }
  }, [layout]);

  return (
    <div className="dashboard-container">
      <div className="top-search-bar">
        <SearchBar onSubmit={handleSearchSubmit} />
      </div>

      <div className="chat-summary-wrapper">
        <ChatSummary
          prompt={prompt}
          slm={slmResponse}
          followUp={followUp}
          loading={loading}
        />
      </div>

      <div className="dashboard-body">
        <div className="sidebar">
          <FilterSidebar
            widgets={widgets}
            visible={visibleWidgets}
            toggle={toggleWidget}
          />
        </div>

        <div className="main-content">
          {loading && <div className="loading">Loading charts...</div>}

          {layout.length > 0 ? (
            layout.map((item, idx) => (
              visibleWidgets[item.title] && (
                <div className="chart-wrapper" key={idx}>
                  <RequestChart
                    title={item.title}
                    promql={item.promql}
                    chartType={item.chart_type}
                    thresholds={item.thresholds}
                  />
                </div>
              )
            ))
          ) : (
            !loading && (
              <div className="no-data">No charts to display. Try a different prompt.</div>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
