import type { WindowNostr } from 'nostr-tools/nip07';
import type { EventTemplate } from 'nostr-tools';

type SignedEvent = Awaited<ReturnType<WindowNostr['signEvent']>>;

export type Nip07Signer = {
	getPublicKey: () => Promise<string>;
	signEvent: (tpl: EventTemplate) => Promise<SignedEvent>;
};

function getWindowNostr(): WindowNostr | null {
	if (typeof window === 'undefined') return null;
	return (window as Window & { nostr?: WindowNostr }).nostr ?? null;
}

export function hasNip07(): boolean {
	return getWindowNostr() !== null;
}

export function getNip07Signer(): Nip07Signer | null {
	const nostr = getWindowNostr();
	if (!nostr) return null;
	return {
		getPublicKey: () => nostr.getPublicKey(),
		signEvent: (tpl) => nostr.signEvent(tpl),
	};
}
