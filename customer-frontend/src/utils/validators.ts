export function validateEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email.trim());
}

export function validatePhone(phone: string): boolean {
  const clean = phone.replace(/[\s\-\+\(\)]/g, '');
  return clean.length >= 10 && clean.length <= 13;
}
