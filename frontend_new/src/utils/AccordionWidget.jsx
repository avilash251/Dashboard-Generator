import React from "react"; import { Accordion, AccordionSummary, AccordionDetails, Typography, Card, CardContent, Box } from "@mui/material"; import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const AccordionWidget = ({ headerName, children, icon = "🧠" }) => { return ( <Accordion defaultExpanded> <AccordionSummary expandIcon={<ExpandMoreIcon />}> <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}> <Typography variant="h5" component="span"> {icon} </Typography> <Typography variant="subtitle1">{headerName}</Typography> </Box> </AccordionSummary> <AccordionDetails> <Card variant="outlined"> <CardContent> {children} </CardContent> </Card> </AccordionDetails> </Accordion> ); };

export default AccordionWidget;

