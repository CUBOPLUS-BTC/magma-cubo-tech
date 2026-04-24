import { PUBLIC_API_URL } from '$env/static/public';

const BASE = PUBLIC_API_URL;

export const endpoints = {
  auth: {
    challenge: `${BASE}/auth/challenge`,
    verify: `${BASE}/auth/verify`,
    me: `${BASE}/auth/me`,
    lnurl: `${BASE}/auth/lnurl`,
    lnurlStatus: (k1: string) => `${BASE}/auth/lnurl-status?k1=${k1}`,
  },
  price: `${BASE}/price`,
  remittance: {
    compare: `${BASE}/remittance/compare`,
    fees: `${BASE}/remittance/fees`,
  },
  savings: {
    project: `${BASE}/savings/project`,
    goal: `${BASE}/savings/goal`,
    deposit: `${BASE}/savings/deposit`,
    progress: `${BASE}/savings/progress`,
  },
  alerts: {
    list: (since: number) => `${BASE}/alerts?since=${since}`,
    status: `${BASE}/alerts/status`,
    preferences: `${BASE}/alerts/preferences`,
  },
  achievements: `${BASE}/achievements`,
  pension: {
    projection: `${BASE}/pension/projection`,
  },
  network: {
    status: `${BASE}/network/status`,
  },
  education: {
    lessons: (locale: string, category?: string, difficulty?: string) => {
      const p = new URLSearchParams({ locale });
      if (category) p.set('category', category);
      if (difficulty) p.set('difficulty', difficulty);
      return `${BASE}/education/lessons?${p}`;
    },
    lesson: (id: string, locale: string) => `${BASE}/education/lesson?id=${id}&locale=${locale}`,
    glossary: (locale: string, q?: string) => {
      const p = new URLSearchParams({ locale });
      if (q) p.set('q', q);
      return `${BASE}/education/glossary?${p}`;
    },
    quiz: `${BASE}/education/quiz`,
    units: (locale: string) => `${BASE}/education/units?locale=${locale}`,
    progress: `${BASE}/education/progress`,
    loseHeart: `${BASE}/education/progress/lose-heart`,
  },
  liquid: {
    overview: `${BASE}/liquid/overview`,
    assets: `${BASE}/liquid/assets`,
    compare: `${BASE}/liquid/compare`,
    pegInfo: `${BASE}/liquid/peg-info`,
    recommend: `${BASE}/liquid/recommend`,
  },
  recipients: {
    list: `${BASE}/recipients`,
    create: `${BASE}/recipients`,
    byId: (id: number) => `${BASE}/recipients/${id}`,
  },
  reminders: {
    list: `${BASE}/reminders`,
    create: `${BASE}/reminders`,
    byId: (id: number) => `${BASE}/reminders/${id}`,
    events: (id: number, limit = 50) => `${BASE}/reminders/${id}/events?limit=${limit}`,
  },
  sends: {
    execute: `${BASE}/sends/execute`,
  },
};