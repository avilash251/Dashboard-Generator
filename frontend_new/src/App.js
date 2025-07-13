import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import ChatPopup from "./components/ChatPopup";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChatPopup />} />
        <Route path="/promethus-dashboard" element={<Dashboard />} />
        {/* Add a fallback route */}
        <Route path="*" element={<h2>404: Page Not Found</h2>} />
      </Routes>
    </Router>
  );
}

export default App;
