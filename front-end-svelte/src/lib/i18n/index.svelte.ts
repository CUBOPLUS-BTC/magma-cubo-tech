import { browser } from '$app/environment';
import { en } from './en';
import { es } from './es';

const translations = { en, es } as const;
type Locale = keyof typeof translations;

function detectLocale(): Locale {
  if (!browser) return 'en';
  const lang = navigator.language.slice(0, 2);
  return lang === 'es' ? 'es' : 'en';
}

let current = $state<Locale>(detectLocale());

export const i18n = {
  get t() { return translations[current]; },
  get locale() { return current; },
  setLocale(locale: Locale) { current = locale; },
};
