import React from 'react';
import '../styles/dashboard.css';

const FilterSidebar = ({ availableWidgets, selectedWidgets, onToggle }) => {
  return (
    <div className="filter-sidebar">
      <h3>Filter Widgets</h3>
      <ul>
        {availableWidgets.map((widget, index) => (
          <li key={index}>
            <label>
              <input
                type="checkbox"
                checked={selectedWidgets.includes(widget.id)}
                onChange={() => onToggle(widget.id)}
              />
              {widget.title}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FilterSidebar;
