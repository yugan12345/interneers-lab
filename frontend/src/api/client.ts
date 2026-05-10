/**
 * API client — all fetch calls to the Django backend live here.
 *
 * Centralising API calls means:
 *   - Components never construct URLs directly
 *   - Changing the base URL or adding auth headers only needs one change
 *   - Each function has a clear return type so TypeScript can help callers
 */

import type {
  PaginatedProducts,
  PaginatedCategories,
  Product,
  Category,
  ProductFilters,
} from "../types";

const API_BASE = process.env.REACT_APP_API_BASE ?? "http://localhost:8000";

// ── helpers ──────────────────────────────────────────────────────────

async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error ?? `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

// ── Products ─────────────────────────────────────────────────────────

export async function fetchProducts(
  page = 1,
  pageSize = 9,
  filters: ProductFilters = {}
): Promise<PaginatedProducts> {
  const params = new URLSearchParams();
  params.set("page", String(page));
  params.set("page_size", String(pageSize));
  if (filters.search)     params.set("search", filters.search);
  if (filters.minPrice)   params.set("min_price", filters.minPrice);
  if (filters.maxPrice)   params.set("max_price", filters.maxPrice);
  if (filters.categoryId) params.set("category_ids", filters.categoryId);
  return apiFetch<PaginatedProducts>(`/products/?${params}`);
}

export async function fetchProduct(id: string): Promise<Product> {
  return apiFetch<Product>(`/products/${id}/`);
}

export async function fetchProductsByCategory(
  categoryId: string
): Promise<{ category: Category; total_products: number; products: Product[] }> {
  return apiFetch(`/categories/${categoryId}/products/`);
}

// ── Categories ───────────────────────────────────────────────────────

export async function fetchCategories(
  pageSize = 50
): Promise<PaginatedCategories> {
  return apiFetch<PaginatedCategories>(`/categories/?page_size=${pageSize}`);
}

export async function fetchCategory(id: string): Promise<Category> {
  return apiFetch<Category>(`/categories/${id}/`);
}