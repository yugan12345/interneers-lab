/**
 * Header — site-wide navigation bar.
 * Week 7 advanced: header and navigation bar.
 * Week 8: nav links use React Router for client-side navigation.
 */

import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";

export default function Header() {
  const location = useLocation();

  const navLinks = [
    { to: "/",           label: "Products" },
    { to: "/categories", label: "Categories" },
  ];

  return (
    <header className="header">
      <div className="header-inner">
        <Link to="/" className="header-logo">
          <span className="header-logo-mark">▣</span>
          <span className="header-logo-text">WAREHOUSE</span>
        </Link>

        <nav className="header-nav">
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className={
                "header-nav-link" +
                (location.pathname === link.to ? " active" : "")
              }
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}