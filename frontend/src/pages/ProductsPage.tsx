/**
 * ProductsPage — the main products listing page at route "/".
 *
 * Week 8: connects FilterBar, ProductList, and Pagination together
 * using the useProducts and useCategories hooks for real API data.
 * Handles loading state, error state, and loading spinners.
 */

import React from "react";
import FilterBar from "../components/FilterBar";
import ProductList from "../components/ProductList";
import Pagination from "../components/Pagination";
import { useProducts } from "../hooks/useProducts";
import { useCategories } from "../hooks/useCategories";
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
  } = useProducts(9);

  const { categories } = useCategories();

  return (
    <div className="products-page">
      <div className="products-page-title-row">
        <h1 className="products-page-title">Products</h1>
        {!loading && (
          <span className="products-page-count">{totalProducts} total</span>
        )}
      </div>

      <FilterBar
        categories={categories}
        onFilterChange={setFilters}
        loading={loading}
      />

      {error && (
        <div className="products-page-error">
          <span className="error-icon">⚠</span>
          {error === "Failed to fetch"
            ? "Could not reach the API — make sure Django is running on localhost:8000"
            : error}
        </div>
      )}

      <ProductList
        products={products}
        loading={loading}
        emptyMessage="No products match your filters"
      />

      <Pagination
        page={page}
        totalPages={totalPages}
        totalProducts={totalProducts}
        onPageChange={setPage}
      />
    </div>
  );
}