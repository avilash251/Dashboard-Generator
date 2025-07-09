import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ChatPopup from './components/ChatPopup';
import FloatingBot from './components/FloatingBot';

function AppWrapper() {
  const [showPopup, setShowPopup] = useState(localStorage.getItem('popupVisible') === 'true');
  const navigate = useNavigate();

  const openPopup = () => {
    setShowPopup(true);
    localStorage.setItem('popupVisible', 'true');
  };

  const closePopup = () => {
    setShowPopup(false);
    localStorage.setItem('popupVisible', 'false');
    navigate('/');
  };

  const maximizePopup = () => {
    setShowPopup(false);
    localStorage.setItem('popupVisible', 'false');
    navigate('/promethus-dashboard');
  };

  return (
    <>
      <FloatingBot onClick={openPopup} />
      {showPopup && <ChatPopup onClose={closePopup} onMaximize={maximizePopup} />}
      <Routes>
        <Route path="/" element={<div />} />
        <Route path="/promethus-dashboard" element={<Dashboard />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}
