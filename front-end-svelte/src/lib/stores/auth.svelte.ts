import { browser } from '$app/environment';
import { nip19, getPublicKey, finalizeEvent, generateSecretKey } from 'nostr-tools';
import type { EventTemplate } from 'nostr-tools';
import { endpoints } from '$lib/api/endpoints';
import { getNip07Signer } from '$lib/nostr/nip07';

const NSEC_STORAGE = 'magma_nsec';
const EVENT_STORAGE = 'magma_auth_event';

type SignedAuthEvent = {
  id: string;
  pubkey: string;
  sig: string;
  kind: number;
  created_at: number;
  tags: string[][];
  content: string;
};

type EventSigner = (tpl: EventTemplate) => Promise<SignedAuthEvent> | SignedAuthEvent;

function decodePrivateKey(input: string): Uint8Array {
  const trimmed = input.trim();
  if (trimmed.startsWith('nsec1')) {
    const decoded = nip19.decode(trimmed);
    if (decoded.type !== 'nsec') throw new Error('Invalid nsec key');
    return decoded.data as Uint8Array;
  }
  if (/^[0-9a-f]{64}$/i.test(trimmed)) {
    const bytes = new Uint8Array(32);
    for (let i = 0; i < 32; i++) bytes[i] = parseInt(trimmed.slice(i * 2, i * 2 + 2), 16);
    return bytes;
  }
  throw new Error('Invalid key format. Use nsec1... or 64-char hex.');
}

function loadStoredPubkey(): string | null {
  if (!browser) return null;
  const nsec = localStorage.getItem(NSEC_STORAGE);
  if (nsec) {
    try { return getPublicKey(decodePrivateKey(nsec)); } catch { /* fall through */ }
  }
  const eventB64 = localStorage.getItem(EVENT_STORAGE);
  if (eventB64) {
    try { return (JSON.parse(atob(eventB64)) as SignedAuthEvent).pubkey; } catch { /* noop */ }
  }
  return null;
}

function createAuth() {
  const initialPubkey = loadStoredPubkey();
  let publicKey = $state<string | null>(initialPubkey);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  async function runAuthFlow(pubkey: string, sign: EventSigner): Promise<SignedAuthEvent> {
    const challengeRes = await fetch(endpoints.auth.challenge, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pubkey }),
    });
    if (!challengeRes.ok) throw new Error('Failed to get challenge');
    const { challenge } = await challengeRes.json();

    const event = await sign({
      kind: 27235,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['u', endpoints.auth.verify],
        ['method', 'POST'],
        ['challenge', challenge],
      ],
      content: '',
    });

    const verifyRes = await fetch(endpoints.auth.verify, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ signed_event: event, challenge }),
    });
    if (!verifyRes.ok) throw new Error('Authentication failed');

    if (browser) localStorage.setItem(EVENT_STORAGE, btoa(JSON.stringify(event)));
    return event;
  }

  return {
    get isAuthenticated() { return !!publicKey; },
    get publicKey() { return publicKey; },
    get isLoading() { return isLoading; },
    get error() { return error; },

    clearError() { error = null; },

    async login(nsecOrHex: string) {
      isLoading = true;
      error = null;
      try {
        const sk = decodePrivateKey(nsecOrHex);
        const pk = getPublicKey(sk);
        await runAuthFlow(pk, (tpl) => finalizeEvent(tpl, sk));
        if (browser) localStorage.setItem(NSEC_STORAGE, nip19.nsecEncode(sk));
        publicKey = pk;
      } catch (e) {
        error = e instanceof Error ? e.message : 'Authentication failed';
        throw e;
      } finally {
        isLoading = false;
      }
    },

    async loginWithExtension() {
      const signer = getNip07Signer();
      if (!signer) {
        error = 'No Nostr extension found. Install nos2x or Alby.';
        throw new Error(error);
      }
      isLoading = true;
      error = null;
      try {
        const pk = await signer.getPublicKey();
        await runAuthFlow(pk, (tpl) => signer.signEvent(tpl));
        publicKey = pk;
      } catch (e) {
        error = e instanceof Error ? e.message : 'Extension login failed';
        throw e;
      } finally {
        isLoading = false;
      }
    },

    generateKeys() {
      const sk = generateSecretKey();
      const pk = getPublicKey(sk);
      return { nsec: nip19.nsecEncode(sk), npub: nip19.npubEncode(pk) };
    },

    logout() {
      publicKey = null;
      if (browser) {
        localStorage.removeItem(NSEC_STORAGE);
        localStorage.removeItem(EVENT_STORAGE);
      }
    },

    getAuthHeader(): string | null {
      if (!browser) return null;
      const eventB64 = localStorage.getItem(EVENT_STORAGE);
      return eventB64 ? `Nostr ${eventB64}` : null;
    },
  };
}

export const auth = createAuth();
