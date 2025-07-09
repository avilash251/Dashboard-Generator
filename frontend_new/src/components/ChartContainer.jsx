import React from 'react';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts';

const ChartContainer = ({ layout, next }) => {
  return (
    <div>
      {layout.map((item, idx) => (
        <div key={idx} style={{ marginBottom: '20px' }}>
          <h4>{item.title}</h4>
          <HighchartsReact highcharts={Highcharts} options={{
            title: { text: item.title },
            series: [{
              data: item.data || [],
              type: item.chart_type || 'line'
            }]
          }} />
        </div>
      ))}
      {next.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h5>💡 You can also ask:</h5>
          <ul>
            {next.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChartContainer;
