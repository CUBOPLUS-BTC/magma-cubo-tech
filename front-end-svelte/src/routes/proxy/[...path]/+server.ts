import { API_URL } from '$env/static/private';
import type { RequestHandler } from '@sveltejs/kit';

const handler: RequestHandler = async ({ params, request }) => {
  const url = `${API_URL}/${params.path}`;

  const headers = new Headers();
  const ct = request.headers.get('content-type');
  if (ct) headers.set('content-type', ct);
  const auth = request.headers.get('authorization');
  if (auth) headers.set('authorization', auth);

  const body = request.method !== 'GET' ? await request.text() : undefined;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);

  try {
    const res = await fetch(url, {
      method: request.method,
      headers,
      body,
      signal: controller.signal,
    });

    const data = await res.text();

    return new Response(data, {
      status: res.status,
      headers: { 'content-type': res.headers.get('content-type') ?? 'application/json' },
    });
  } catch {
    return new Response(JSON.stringify({ error: 'Backend timeout' }), {
      status: 504,
      headers: { 'content-type': 'application/json' },
    });
  } finally {
    clearTimeout(timeout);
  }
};

export const GET = handler;
export const POST = handler;
