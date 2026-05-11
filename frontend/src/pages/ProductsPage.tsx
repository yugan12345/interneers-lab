/**
 * ProductsPage — the main products listing page at route "/".
 *
 * Week 8: connects FilterBar, ProductList, and Pagination together
 * using the useProducts and useCategories hooks for real API data.
 * Handles loading state, error state, loading spinners, and full CRUD.
 */

import React, { useState } from "react";
import FilterBar from "../components/FilterBar";
import ProductList from "../components/ProductList";
import Pagination from "../components/Pagination";
import ProductForm from "../components/ProductForm";
import { useProducts } from "../hooks/useProducts";
import { useCategories } from "../hooks/useCategories";
import { createProduct, updateProduct, deleteProduct } from "../api/client";
import type { Product, ProductPayload } from "../types";
import "./ProductsPage.css";

export default function ProductsPage() {
  const {
    products,
    loading,
    error,
    page,
    totalPages,
    totalProducts,
    setPage,
    setFilters,
    refresh,
  } = useProducts(9);

  const { categories } = useCategories();

  // null = form closed | undefined = creating new | Product = editing existing
  const [formProduct, setFormProduct] = useState<Product | undefined | null>(null);
  const [saving, setSaving] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function handleSave(data: ProductPayload) {
    setSaving(true);
    setActionError(null);
    try {
      if (formProduct?.id) {
        await updateProduct(formProduct.id, data);
      } else {
        await createProduct(data);
      }
      setFormProduct(null);
      refresh();
    } catch (e: any) {
      setActionError(e.message ?? "Save failed");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(product: Product) {
    if (!window.confirm(`Delete "${product.name}"?`)) return;
    setActionError(null);
    try {
      await deleteProduct(product.id);
      refresh();
    } catch (e: any) {
      setActionError(e.message ?? "Delete failed");
    }
  }

  return (
    <div className="products-page">
      <div className="products-page-title-row">
        <h1 className="products-page-title">Products</h1>
        {!loading && (
          <span className="products-page-count">{totalProducts} total</span>
        )}
        <button
          className="btn-primary"
          onClick={() => setFormProduct(undefined)}
        >
          + New Product
        </button>
      </div>

      <FilterBar
        categories={categories}
        onFilterChange={setFilters}
        loading={loading}
      />

      {(error || actionError) && (
        <div className="products-page-error">
          <span className="error-icon">⚠</span>
          {error === "Failed to fetch"
            ? "Could not reach the API — make sure Django is running on localhost:8000"
            : error ?? actionError}
        </div>
      )}

      <ProductList
        products={products}
        loading={loading}
        emptyMessage="No products match your filters"
        onEdit={(p) => setFormProduct(p)}
        onDelete={handleDelete}
      />

      <Pagination
        page={page}
        totalPages={totalPages}
        totalProducts={totalProducts}
        onPageChange={setPage}
      />

      {formProduct !== null && (
        <ProductForm
          product={formProduct}
          categories={categories}
          saving={saving}
          onSave={handleSave}
          onClose={() => setFormProduct(null)}
        />
      )}
    </div>
  );
}