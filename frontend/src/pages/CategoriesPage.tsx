/**
 * CategoriesPage — lists all product categories at route "/categories".
 * Week 8 advanced: clicking a category shows its products.
 */

import React, { useState } from "react";
import { useCategories } from "../hooks/useCategories";
import { fetchProductsByCategory } from "../api/client";
import type { Category, Product } from "../types";
import ProductList from "../components/ProductList";
import "./CategoriesPage.css";

function CategoryCard({
  category,
  isSelected,
  onClick,
}: {
  category: Category;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <div
      className={`category-card ${isSelected ? "selected" : ""}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === "Enter" && onClick()}
    >
      <div className="category-card-title">{category.title}</div>
      <div className="category-card-desc">{category.description}</div>
      <div className="category-card-hint">
        {isSelected ? "▲ hide products" : "▼ view products"}
      </div>
    </div>
  );
}

export default function CategoriesPage() {
  const { categories, loading, error } = useCategories();
  const [selectedId, setSelectedId]     = useState<string | null>(null);
  const [catProducts, setCatProducts]   = useState<Product[]>([]);
  const [catLoading, setCatLoading]     = useState(false);

  async function handleCategoryClick(category: Category) {
    if (selectedId === category.id) {
      setSelectedId(null);
      setCatProducts([]);
      return;
    }
    setSelectedId(category.id);
    setCatLoading(true);
    try {
      const data = await fetchProductsByCategory(category.id);
      setCatProducts(data.products);
    } catch {
      setCatProducts([]);
    } finally {
      setCatLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="categories-page">
        <h1 className="categories-page-title">Categories</h1>
        <div className="categories-grid">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="category-card-skeleton" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="categories-page">
        <h1 className="categories-page-title">Categories</h1>
        <div className="categories-error">⚠ {error}</div>
      </div>
    );
  }

  return (
    <div className="categories-page">
      <div className="categories-page-title-row">
        <h1 className="categories-page-title">Categories</h1>
        <span className="categories-page-count">{categories.length} total</span>
      </div>

      <div className="categories-grid">
        {categories.map(cat => (
          <CategoryCard
            key={cat.id}
            category={cat}
            isSelected={selectedId === cat.id}
            onClick={() => handleCategoryClick(cat)}
          />
        ))}
      </div>

      {selectedId && (
        <div className="categories-products-section">
          <div className="categories-products-label">
            PRODUCTS IN{" "}
            {categories.find(c => c.id === selectedId)?.title.toUpperCase()}
          </div>
          <ProductList
            products={catProducts}
            loading={catLoading}
            emptyMessage="No products in this category"
          />
        </div>
      )}
    </div>
  );
}