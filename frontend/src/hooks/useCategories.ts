/**
 * Custom hook: useCategories
 * Fetches all categories once on mount — used to populate filter dropdowns.
 */

import { useState, useEffect } from "react";
import { fetchCategories } from "../api/client";
import type { Category } from "../types";

interface UseCategoriesResult {
  categories: Category[];
  loading: boolean;
  error: string | null;
}

export function useCategories(): UseCategoriesResult {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading]       = useState(true);
  const [error, setError]           = useState<string | null>(null);

  useEffect(() => {
    fetchCategories()
      .then(data => setCategories(data.categories))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { categories, loading, error };
}