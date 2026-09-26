import { type ClassValue, clsx } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return inputs.filter(Boolean).join(' ');
}

export function formatIndianNumber(num: number): string {
  if (Math.abs(num) >= 10000000) {
    return (num / 10000000).toFixed(1) + ' Cr';
  }
  if (Math.abs(num) >= 100000) {
    return (num / 100000).toFixed(1) + ' Lakh';
  }
  return num.toLocaleString('en-IN');
}
