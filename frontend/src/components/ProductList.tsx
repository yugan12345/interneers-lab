/**
 * ProductList — renders a grid of product cards.
 * Clicking a card expands inline to show full product details.
 *
 * Week 7: component structure with dummy data fallback.
 * Week 8: receives real products from useProducts hook via parent.
 *
 * Pattern used here:
 *   - selectedId state tracks which card is expanded
 *   - clicking the same card again collapses it (toggle)
 *   - the expanded detail renders below the clicked card's row
 */

import React, { useState } from "react";
import type { Product } from "../types";
import ProductDetail from "./Product";
import "./ProductList.css";

interface Props {
  products: Product[];
  loading?: boolean;
  emptyMessage?: string;
  onEdit?: (product: Product) => void;
  onDelete?: (product: Product) => void;
}

// Dummy data used in Week 7 when no real products are passed
const DUMMY_PRODUCTS: Product[] = [
  {
    id: "dummy-1",
    name: "MacBook Pro 16\"",
    description: "Apple M3 Pro chip, 18GB RAM, 512GB SSD. Perfect for developers.",
    price: 2499.99,
    brand: "Apple",
    quantity: 12,
    category: { id: "cat-1", title: "Electronics" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "dummy-2",
    name: "iPhone 15 Pro",
    description: "Titanium design, A17 Pro chip, 48MP camera system.",
    price: 999.99,
    brand: "Apple",
    quantity: 45,
    category: { id: "cat-1", title: "Electronics" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "dummy-3",
    name: "Sony WH-1000XM5",
    description: "Industry-leading noise cancelling headphones with 30hr battery.",
    price: 349.99,
    brand: "Sony",
    quantity: 3,
    category: { id: "cat-1", title: "Electronics" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "dummy-4",
    name: "Organic Sourdough Bread",
    description: "Stone-milled wheat, slow-fermented 24 hours. Baked fresh daily.",
    price: 6.99,
    brand: "Local Bakery",
    quantity: 80,
    category: { id: "cat-2", title: "Food" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "dummy-5",
    name: "Cast Iron Skillet 12\"",
    description: "Pre-seasoned cast iron, even heat distribution, oven safe to 500°F.",
    price: 44.99,
    brand: "Lodge",
    quantity: 22,
    category: { id: "cat-3", title: "Kitchen Essentials" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "dummy-6",
    name: "USB-C Hub 7-in-1",
    description: "4K HDMI, 100W PD, 3× USB-A, SD card reader, ethernet.",
    price: 49.99,
    brand: "Anker",
    quantity: 2,
    category: { id: "cat-1", title: "Electronics" },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

function ProductCard({
  product,
  isSelected,
  onClick,
}: {
  product: Product;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <div
      className={`product-card ${isSelected ? "selected" : ""}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === "Enter" && onClick()}
      aria-expanded={isSelected}
    >
      <div className="product-card-category">
        {product.category?.title ?? "Uncategorized"}
      </div>
      <div className="product-card-name">{product.name}</div>
      <div className="product-card-desc">{product.description}</div>
      <div className="product-card-footer">
        <span className="product-card-price">
          ${product.price.toFixed(2)}
        </span>
        <span className={`product-card-stock ${product.quantity <= 5 ? "low" : ""}`}>
          <span className="stock-dot" />
          {product.quantity} in stock
        </span>
      </div>
      <div className="product-card-expand-hint">
        {isSelected ? "▲ collapse" : "▼ details"}
      </div>
    </div>
  );
}

export default function ProductList({
  products,
  loading = false,
  emptyMessage = "No products found",
  onEdit,
  onDelete,
}: Props) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const displayProducts = products.length > 0 ? products : (!loading ? DUMMY_PRODUCTS : []);
  const selectedProduct = displayProducts.find(p => p.id === selectedId) ?? null;

  function handleCardClick(id: string) {
    setSelectedId(prev => (prev === id ? null : id));
  }

  if (loading) {
    return (
      <div className="product-list-grid">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="product-card-skeleton" />
        ))}
      </div>
    );
  }

  if (displayProducts.length === 0) {
    return (
      <div className="product-list-empty">
        <div className="product-list-empty-icon">◈</div>
        <div className="product-list-empty-text">{emptyMessage}</div>
      </div>
    );
  }

  return (
    <div className="product-list-wrap">
      <div className="product-list-grid">
        {displayProducts.map(product => (
          <ProductCard
            key={product.id}
            product={product}
            isSelected={selectedId === product.id}
            onClick={() => handleCardClick(product.id)}
          />
        ))}
      </div>

      {selectedProduct && (
        <ProductDetail
          product={selectedProduct}
          onClose={() => setSelectedId(null)}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      )}
    </div>
  );
}