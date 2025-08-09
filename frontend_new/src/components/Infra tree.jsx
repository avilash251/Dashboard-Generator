// src/components/InfraTree.jsx
import * as React from "react";
import { Box, Typography } from "@mui/material";
import { TreeView, TreeItem } from "@mui/lab";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

function renderLeaf(label, nodeId, payload, onSelect) {
  return (
    <TreeItem
      key={nodeId}
      nodeId={nodeId}
      label={
        <Box sx={{ display: "flex", flexDirection: "column" }}>
          <Typography variant="body2" sx={{ fontWeight: 500 }}>{label}</Typography>
          {payload && (
            <Typography variant="caption" color="text.secondary">
              {payload.subtitle ?? ""}
            </Typography>
          )}
        </Box>
      }
      onClick={(e) => {
        e.stopPropagation();
        onSelect?.({ type: "leaf", nodeId, label, payload });
      }}
    />
  );
}

export default function InfraTree({
  data,
  title = "Infrastructure",
  defaultExpanded = ["infra", "infra:tkgi", "infra:ocp"],
  onSelect, // callback({ type, nodeId, label, payload })
}) {
  // data shape (example):
  // {
  //   tkgi: [{id:"tkgi:cluster-a", name:"Cluster A", subtitle:"12 nodes, 64 CPUs"}],
  //   ocp:  [{id:"ocp:prod", name:"OCP Prod", subtitle:"8 nodes"}],
  //   tas: [], onprem: [], database: [], network: [], gcp: [], azure: []
  // }

  const groups = [
    "tkgi",
    "ocp",
    "tas",
    "on-prem",
    "database",
    "network",
    "gcp",
    "azure",
  ];

  return (
    <Box sx={{ p: 1 }}>
      <Typography variant="subtitle2" sx={{ mb: 1, color: "text.secondary" }}>
        {title}
      </Typography>

      <TreeView
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        defaultExpanded={defaultExpanded}
      >
        <TreeItem nodeId="infra" label="Infra">
          {groups.map((group) => {
            const key = group.replace("-", "");
            const items = data?.[key] ?? [];
            return (
              <TreeItem
                key={`infra:${group}`}
                nodeId={`infra:${group}`}
                label={`${group.toUpperCase()}${items.length ? ` (${items.length})` : ""}`}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelect?.({ type: "group", nodeId: `infra:${group}`, label: group });
                }}
              >
                {items.length === 0
                  ? renderLeaf("— none —", `infra:${group}:none`)
                  : items.map((it, idx) =>
                      renderLeaf(
                        it.name ?? it.id ?? `${group}-${idx}`,
                        it.id ?? `infra:${group}:${idx}`,
                        it,
                        onSelect
                      )
                    )}
              </TreeItem>
            );
          })}
        </TreeItem>
      </TreeView>
    </Box>
  );
}
