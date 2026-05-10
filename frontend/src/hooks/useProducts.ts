/**
 * Custom hook: useProducts
 *
 * Encapsulates all state and fetching logic for the products list.
 * Components that need products just call this hook — they don't care
 * about fetch(), loading state, or error handling.
 *
 * This is the React pattern for separating data-fetching from rendering.
 */

import { useState, useEffect, useCallback } from "react";
import { fetchProducts } from "../api/client";
import type { Product, PaginatedProducts, ProductFilters } from "../types";

interface UseProductsResult {
  products: Product[];
  loading: boolean;
  error: string | null;
  page: number;
  totalPages: number;
  totalProducts: number;
  setPage: (page: number) => void;
  setFilters: (filters: ProductFilters) => void;
  refresh: () => void;
}

export function useProducts(pageSize = 9): UseProductsResult {
  const [products, setProducts]         = useState<Product[]>([]);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState<string | null>(null);
  const [page, setPage]                 = useState(1);
  const [totalPages, setTotalPages]     = useState(1);
  const [totalProducts, setTotalProducts] = useState(0);
  const [filters, setFilters]           = useState<ProductFilters>({});
  const [refreshKey, setRefreshKey]     = useState(0);

  const refresh = useCallback(() => setRefreshKey(k => k + 1), []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchProducts(page, pageSize, filters)
      .then((data: PaginatedProducts) => {
        if (cancelled) return;
        setProducts(data.products);
        setTotalPages(data.total_pages);
        setTotalProducts(data.total_products);
      })
      .catch((err: Error) => {
        if (cancelled) return;
        setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [page, pageSize, filters, refreshKey]);

  const handleSetFilters = useCallback((f: ProductFilters) => {
    setFilters(f);
    setPage(1); // reset to page 1 when filters change
  }, []);

  return {
    products,
    loading,
    error,
    page,
    totalPages,
    totalProducts,
    setPage,
    setFilters: handleSetFilters,
    refresh,
  };
}