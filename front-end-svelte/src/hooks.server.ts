import type { HandleServerError } from '@sveltejs/kit';

export const handleError: HandleServerError = async ({ error, status, message }) => {
  console.error(`[${status}]`, message, error);

  return {
    message: status === 404 ? 'Page not found' : 'An unexpected error occurred',
    code: `E${status}`,
  };
};
