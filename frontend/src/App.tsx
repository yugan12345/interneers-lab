/**
 * App.tsx — root component, sets up routing.
 *
 * Week 7: structure with Header, nav links, and page components.
 * Week 8: pages connected to real API via custom hooks.
 *
 * Routes:
 *   /             → ProductsPage (product grid with filters)
 *   /categories   → CategoriesPage (category list, click to see products)
 *   *             → 404 not found
 */

import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ProductsPage from "./pages/ProductsPage";
import CategoriesPage from "./pages/CategoriesPage";
import "./App.css";

function NotFound() {
  return (
    <div
      style={{
        maxWidth: 1400,
        margin: "0 auto",
        padding: "80px 32px",
        textAlign: "center",
        fontFamily: "'Syne', sans-serif",
      }}
    >
      <div style={{ fontSize: 48, color: "#2a2a2a", marginBottom: 16 }}>◈</div>
      <h2 style={{ fontSize: 24, color: "#3d3d3d", marginBottom: 8 }}>
        404 — Page not found
      </h2>
      <a
        href="/"
        style={{
          color: "#e8ff47",
          fontSize: 13,
          fontFamily: "'DM Mono', monospace",
        }}
      >
        ← Back to products
      </a>
    </div>
  );
}

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<ProductsPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}
