// src/components/LayoutRenderer.jsx

import React from "react";
import SummaryPanel from "./SummaryPanel";
import HealthPanel from "./HealthPanel";
import StatsCardPanel from "./StatsCardPanel";
import ChartPanel from "./ChartPanel";

const widgetOrder = ["summary", "health", "statsCard", "charts"];

const LayoutRenderer = ({ visibleSections, summary, layout }) => {
  return (
    <>
      {widgetOrder.map((sectionKey) => {
        if (!visibleSections[sectionKey]) return null;

        switch (sectionKey) {
          case "summary":
            return summary && summary.trim().length > 0 ? (
              <SummaryPanel key="summary" summary={summary} />
            ) : null;

          case "health":
            return layout.health?.length > 0 ? (
              <HealthPanel key="health" data={layout.health} />
            ) : null;

          case "statsCard":
            return layout.statsCard?.length > 0 ? (
              <StatsCardPanel key="statsCard" data={layout.statsCard} />
            ) : null;

          case "charts":
            return layout.charts?.length > 0 ? (
              <ChartPanel key="charts" data={layout.charts} />
            ) : null;

          default:
            return null;
        }
      })}
    </>
  );
};

export default LayoutRenderer;
