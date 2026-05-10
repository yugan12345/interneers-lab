/**
 * FilterBar — search and filter controls for the product list.
 * Week 8: connects to useProducts hook via onFilterChange callback.
 */

import React, { useState } from "react";
import type { Category, ProductFilters } from "../types";
import "./FilterBar.css";

interface Props {
  categories: Category[];
  onFilterChange: (filters: ProductFilters) => void;
  loading?: boolean;
}

export default function FilterBar({ categories, onFilterChange, loading }: Props) {
  const [search, setSearch]       = useState("");
  const [minPrice, setMinPrice]   = useState("");
  const [maxPrice, setMaxPrice]   = useState("");
  const [categoryId, setCategoryId] = useState("");

  function handleApply() {
    const filters: ProductFilters = {};
    if (search)     filters.search     = search;
    if (minPrice)   filters.minPrice   = minPrice;
    if (maxPrice)   filters.maxPrice   = maxPrice;
    if (categoryId) filters.categoryId = categoryId;
    onFilterChange(filters);
  }

  function handleClear() {
    setSearch("");
    setMinPrice("");
    setMaxPrice("");
    setCategoryId("");
    onFilterChange({});
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter") handleApply();
  }

  return (
    <div className="filter-bar">
      <div className="filter-search-wrap">
        <span className="filter-search-icon">⌕</span>
        <input
          type="text"
          className="filter-input filter-search"
          placeholder="Search products…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>

      <input
        type="number"
        className="filter-input filter-price"
        placeholder="Min price"
        value={minPrice}
        min={0}
        onChange={e => setMinPrice(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <span className="filter-sep">—</span>

      <input
        type="number"
        className="filter-input filter-price"
        placeholder="Max price"
        value={maxPrice}
        min={0}
        onChange={e => setMaxPrice(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <select
        className="filter-input filter-select"
        value={categoryId}
        onChange={e => setCategoryId(e.target.value)}
      >
        <option value="">All categories</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>
            {cat.title}
          </option>
        ))}
      </select>

      <button
        className="filter-btn filter-btn-apply"
        onClick={handleApply}
        disabled={loading}
      >
        {loading ? "Loading…" : "Apply →"}
      </button>

      <button
        className="filter-btn filter-btn-clear"
        onClick={handleClear}
      >
        Clear
      </button>
    </div>
  );
}