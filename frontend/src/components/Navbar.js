import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ showNavbar }) => {
  const [isActive, setIsActive] = useState(false);
  const toggleMenu = () => setIsActive(!isActive);

  return (
    <nav className={`navbar ${isActive ? 'active' : ''}`}>
      <div className="logo">Crop & Soil Management</div>
      <div className="menu-toggle" onClick={toggleMenu}>&#9776;</div>
      <ul className={`nav-links ${showNavbar ? 'visible' : ''}`}>
        <li className="nav-item"><Link to="/" onClick={toggleMenu}>Home</Link></li>
        {/* Non-functional links for Weather and Pest Detection */}
        <li className="nav-item"><span onClick={toggleMenu} className="disabled-link">Weather</span></li>
        <li className="nav-item"><span onClick={toggleMenu} className="disabled-link">Pest Detection</span></li>
      </ul>
    </nav>
  );
};

export default Navbar;
