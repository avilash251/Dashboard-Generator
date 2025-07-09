import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import '../styles/widget.css';

const WidgetCard = ({ title, value, unit, chartData, thresholds = {}, showAnomaly = false }) => {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    if (showAnomaly && chartData?.length) {
      const values = chartData.map(d => d.y);
      const mean = values.reduce((a, b) => a + b, 0) / values.length;
      const std = Math.sqrt(values.map(v => (v - mean) ** 2).reduce((a, b) => a + b) / values.length);
      const outliers = chartData.filter(point => Math.abs(point.y - mean) > 2 * std);
      setAnomalies(outliers.map(a => a.x));
    }
  }, [chartData, showAnomaly]);

  const chartOptions = {
    title: { text: title },
    xAxis: { type: 'datetime' },
    yAxis: { title: { text: unit || 'value' } },
    series: [{
      name: title,
      data: chartData,
      color: '#007bff'
    },
    ...(showAnomaly && anomalies.length > 0 ? [{
      type: 'scatter',
      name: 'Anomalies',
      color: 'red',
      data: chartData.filter(d => anomalies.includes(d.x))
    }] : [])
    ],
    credits: { enabled: false }
  };

  const getThresholdBadge = () => {
    if (!thresholds) return null;
    const level = thresholds?.critical ? 'critical' : thresholds?.warning ? 'warning' : null;
    if (!level) return null;

    let className = 'badge';
    let text = '';

    if (value >= thresholds.critical) {
      className += ' danger';
      text = 'Critical';
    } else if (value >= thresholds.warning) {
      className += ' warning';
      text = 'Warning';
    }

    return text ? <span className={className}>{text}</span> : null;
  };

  return (
    <div className="widget-card">
      <div className="widget-header">
        <h4>{title}</h4>
        {getThresholdBadge()}
      </div>
      <div className="widget-value">
        <strong>{value}</strong> <small>{unit}</small>
      </div>
      <HighchartsReact highcharts={Highcharts} options={chartOptions} />
    </div>
  );
};

export default WidgetCard;
