export function isValidBtcAddress(address: string): boolean {
  return /^(bc1q[a-z0-9]{38,58}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$/.test(address);
}
