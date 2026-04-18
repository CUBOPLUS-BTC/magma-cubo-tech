import { endpoints } from '$lib/api/endpoints';
import type { VerifiedPrice } from '$lib/models/price';
import type { NetworkStatus } from '$lib/models/network';

function fetchWithTimeout(fetch: typeof globalThis.fetch, url: string, ms = 5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), ms);
  return fetch(url, { signal: controller.signal }).finally(() => clearTimeout(id));
}

export async function load({ fetch }) {
  const [price, network] = await Promise.all([
    fetchWithTimeout(fetch, endpoints.price)
      .then(r => r.ok ? r.json() as Promise<VerifiedPrice> : null).catch(() => null),
    fetchWithTimeout(fetch, endpoints.network.status)
      .then(r => r.ok ? r.json() as Promise<NetworkStatus> : null).catch(() => null),
  ]);

  return { price, network };
}
