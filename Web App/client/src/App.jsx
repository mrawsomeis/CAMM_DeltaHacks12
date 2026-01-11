import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Consent from './pages/Consent';
import Register from './pages/Register';
import Alerts from './pages/Alerts';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="container">
            <div className="nav-content">
              <Link to="/" className="logo">
                CAMM
              </Link>
              <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/register">Register</Link>
                <Link to="/alerts">Alerts</Link>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/consent" element={<Consent />} />
            <Route path="/register" element={<Register />} />
            <Route path="/alerts" element={<Alerts />} />
          </Routes>
        </main>

        <footer className="footer">
          <div className="container">
            <p>&copy; 2024 CAMM - Community Assistive Monitor Model. Helping communities support each other.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
