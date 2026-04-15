import { browser } from '$app/environment';

const STORAGE_KEY = 'magma_auth';

function createAuth() {
  let isAuthenticated = $state(
    browser ? localStorage.getItem(STORAGE_KEY) === 'true' : false
  );

  return {
    get isAuthenticated() { return isAuthenticated; },

    login() {
      isAuthenticated = true;
      if (browser) localStorage.setItem(STORAGE_KEY, 'true');
    },

    logout() {
      isAuthenticated = false;
      if (browser) localStorage.removeItem(STORAGE_KEY);
    },
  };
}

export const auth = createAuth();
