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
