import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ChatPopup from './components/ChatPopup';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/prometheus-dashboard" element={<Dashboard />} />
        {/* Default page */}
        <Route path="/" element={
          <>
            <ChatPopup onExpand={() => window.location.href = "/prometheus-dashboard"} />
          </>
        } />
      </Routes>
    </Router>
  );
}

export default App;
