export function formatUSD(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

export function formatBTC(value: number): string {
  return `₿ ${value.toFixed(8)}`;
}

export function formatPercent(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

export function formatSatVb(value: number): string {
  return `${value} sat/vB`;
}
