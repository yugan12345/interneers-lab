/**
 * Product — displays a single product's full details.
 *
 * Week 7: component populated with dummy data for layout.
 * Week 8: receives real Product data from parent or router params.
 *
 * Used in two contexts:
 *   1. As an expanded detail view inside ProductList (click to expand)
 *   2. As a standalone page at /products/:id
 */

import React from "react";
import type { Product as ProductType } from "../types";
import "./Product.css";

interface Props {
  product: ProductType;
  onClose?: () => void;
  onEdit?: (product: ProductType) => void;
  onDelete?: (product: ProductType) => void;
}

function formatPrice(price: number): string {
  return "$" + price.toFixed(2);
}

export default function Product({ product, onClose, onEdit, onDelete }: Props) {
  const isLowStock = product.quantity <= 5;

  return (
    <div className="product-detail">
      <div className="product-detail-header">
        <div className="product-detail-category">{product.category?.title ?? "Uncategorized"}</div>
        <div className="product-detail-header-actions">
          {onEdit && (
            <button className="btn-edit" onClick={() => onEdit(product)}>
              Edit
            </button>
          )}
          {onDelete && (
            <button className="btn-delete" onClick={() => onDelete(product)}>
              Delete
            </button>
          )}
          {onClose && (
            <button className="product-detail-close" onClick={onClose}>
              ✕
            </button>
          )}
        </div>
      </div>

      <h2 className="product-detail-name">{product.name}</h2>
      <p className="product-detail-desc">{product.description}</p>

      <div className="product-detail-grid">
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">Price</span>
          <span className="product-detail-stat-value accent">{formatPrice(product.price)}</span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">Brand</span>
          <span className="product-detail-stat-value">{product.brand}</span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">In Stock</span>
          <span className={`product-detail-stat-value ${isLowStock ? "danger" : ""}`}>
            {product.quantity}
            {isLowStock && <span className="low-stock-badge">LOW</span>}
          </span>
        </div>
        <div className="product-detail-stat">
          <span className="product-detail-stat-label">ID</span>
          <span className="product-detail-stat-value muted">{product.id}</span>
        </div>
      </div>

      <div className="product-detail-dates">
        <span>Added {new Date(product.created_at).toLocaleDateString()}</span>
        <span>Updated {new Date(product.updated_at).toLocaleDateString()}</span>
      </div>
    </div>
  );
}
