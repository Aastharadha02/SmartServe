/**
 * Format currency strictly in Indian Rupee (₹)
 */
export function formatRupee(amount?: number | null): string {
  if (amount === undefined || amount === null || isNaN(amount)) return '₹0';
  return `₹${Math.round(amount).toLocaleString('en-IN')}`;
}

export function formatPercent(val?: number | null): string {
  if (val === undefined || val === null || isNaN(val)) return '0%';
  const num = val > 1 ? val : val * 100;
  return `${Math.round(num)}%`;
}

export function formatCategoryDisplayName(name?: string | null): string {
  if (!name) return '';
  return name.replace(/^\d+\.\s*/, '').trim();
}
