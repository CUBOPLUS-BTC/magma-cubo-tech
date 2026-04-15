import { api } from '$lib/api/client';
import { endpoints } from '$lib/api/endpoints';
import type { VerifiedPrice } from '$lib/models/price';

export async function load({ fetch: _fetch }) {
  try {
    const price = await api.get<VerifiedPrice>(endpoints.price);
    return { price };
  } catch {
    return { price: null };
  }
}
