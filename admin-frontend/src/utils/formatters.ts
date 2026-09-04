/**
 * Canonical Currency & Financial Formatters for SmartServe Admin Application (Indian Rupee - ₹ / INR)
 */

export const formatCurrencyINR = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '₹0.00';
  return `₹${Number(val).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

export const formatRupee = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '₹0';
  return `₹${Math.round(Number(val)).toLocaleString('en-IN')}`;
};

export const formatSurgePercent = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '+0% Surge';
  const num = Number(val);
  const pct = num > 1 ? num : num * 100;
  return `+${Math.round(pct)}% Surge`;
};

export const formatDiscountPercent = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '-0% Discount';
  const num = Number(val);
  const pct = num > 1 ? num : num * 100;
  return `-${Math.round(pct)}% Discount`;
};

export const formatCategoryDisplayName = (category: string | null | undefined): string => {
  if (!category) return 'General';
  return category.replace(/^\d+\.\s*/, '').trim();
};
