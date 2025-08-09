// src/pages/Dashboard.jsx
import React, { useMemo, useState } from "react";
import { Grid, Box } from "@mui/material";
import InfraTree from "@/components/InfraTree";
import { adaptInfra } from "@/utils/infraAdapter";
import LayoutRenderer from "@/components/LayoutRenderer"; // your existing renderer

export default function Dashboard({ summary, layout, visibleSections }) {
  const [selection, setSelection] = useState(null); // store selected node/group
  const infraData = useMemo(() => adaptInfra(layout), [layout]);

  const handleTreeSelect = (evt) => {
    // evt = { type: "group"|"leaf", nodeId, label, payload }
    setSelection(evt);
    // Optional: trigger filtering in your panels via Redux or parent state
    // e.g., setFilters({ infraType: evt.type === "group" ? evt.label : evt.payload?.raw?.type, id: evt.payload?.raw?.id })
  };

  return (
    <Grid container spacing={2}>
      {/* Left sidebar ~15% */}
      <Grid item xs={12} md={2} lg={2}>
        <Box sx={{ position: "sticky", top: 8 }}>
          <InfraTree data={infraData} onSelect={handleTreeSelect} />
        </Box>
      </Grid>

      {/* Main content */}
      <Grid item xs={12} md={10} lg={10}>
        <LayoutRenderer
          summary={summary}
          layout={layout}
          visibleSections={visibleSections}
          // Optionally pass selection to filter charts/health/stats
          selection={selection}
        />
      </Grid>
    </Grid>
  );
}
