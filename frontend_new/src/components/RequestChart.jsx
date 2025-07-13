import React, { useEffect, useRef } from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import PropTypes from "prop-types";

const RequestChart = ({ title, data, chartType = "line" }) => {
  const chartComponentRef = useRef(null);

  const options = {
    chart: {
      type: chartType,
      height: 300,
    },
    title: {
      text: title,
      align: "left",
    },
    xAxis: {
      type: "datetime",
      title: {
        text: "Time",
      },
    },
    yAxis: {
      title: {
        text: "Value",
      },
    },
    tooltip: {
      shared: true,
      crosshairs: true,
    },
    series: data || [],
    credits: {
      enabled: false,
    },
  };

  useEffect(() => {
    if (chartComponentRef.current) {
      chartComponentRef.current.chart.reflow();
    }
  }, [data]);

  return (
    <div className="chart-wrapper">
      <HighchartsReact
        highcharts={Highcharts}
        options={options}
        ref={chartComponentRef}
      />
    </div>
  );
};

RequestChart.propTypes = {
  title: PropTypes.string.isRequired,
  data: PropTypes.arrayOf(PropTypes.object),
  chartType: PropTypes.string,
};

export default RequestChart;
