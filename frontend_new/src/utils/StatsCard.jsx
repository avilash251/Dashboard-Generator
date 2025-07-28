// src/components/StatsCard.jsx
import React from "react";
import { Grid, Card, Typography, Box } from "@mui/material";

const colorPalette = [
  "#1E88E5", // Blue
  "#FB8C00", // Orange
  "#8E24AA", // Purple
  "#43A047", // Green
  "#F4511E", // Red
];

const getUnit = (label) => {
  const lower = label.toLowerCase();
  if (lower.includes("memory") || lower.includes("ram")) return "GB";
  if (lower.includes("cpu") || lower.includes("cores")) return "Cores";
  if (lower.includes("usage") || lower.includes("percent")) return "%";
  if (lower.includes("disk")) return "GB";
  return "";
};

const StatsCard = ({ rows }) => {
  if (!rows || Object.keys(rows).length === 0) return null;

  const entries = Object.entries(rows);

  return (
    <Grid container spacing={2}>
      {entries.map(([label, value], idx) => {
        const unit = getUnit(label);
        const color = colorPalette[idx % colorPalette.length];

        return (
          <Grid item xs={6} sm={4} md={3} key={label}>
            <Card
              sx={{
                backgroundColor: color,
                color: "white",
                p: 2,
                borderRadius: 2,
                textAlign: "center",
                boxShadow: 3,
              }}
            >
              <Typography variant="subtitle1" sx={{ fontWeight: "bold" }}>
                {label}
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: "bold", mt: 1 }}>
                {value} {unit}
              </Typography>
            </Card>
          </Grid>
        );
      })}
    </Grid>
  );
};

export default StatsCard;
