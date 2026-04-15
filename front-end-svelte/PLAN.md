# PLAN.md — Migración Magma: Flutter → SvelteKit + shadcn-svelte

> **Este plan está diseñado para ser ejecutado por modelos de generación de código (Gemini 2.5, etc.).**
> Cada tarea es autocontenida, con código exacto y sin ambigüedades. Seguir en orden.

---

## Contexto del proyecto

**App**: Magma — Bitcoin Financial Intelligence
**Migración**: Flutter → SvelteKit (solo frontend, el backend API ya existe)
**Fase actual**: DISEÑO + INTEGRACIÓN (sin autenticación Nostr por ahora)

### Stack ya instalado

| Tecnología | Versión | Propósito |
|---|---|---|
| SvelteKit | 2.57+ | Framework (Svelte 5, runes mode forzado) |
| Tailwind CSS | 4.2 | Estilos (via `@tailwindcss/vite`) |
| shadcn-svelte | 1.2.7 | Componentes UI (estilo Lyra) |
| phosphor-svelte | 3.1 | Iconos (ya instalado por preset) |
| mode-watcher | 1.1 | Dark/light mode (ya configurado en layout raíz) |
| Bun | 1.3 | Package manager |

### Decisiones de arquitectura — NO CAMBIAR

| Categoría | Decisión | Razón |
|---|---|---|
| HTTP Client | **fetch nativo** de SvelteKit | Integrado con load functions, SSR, 0 deps. NO instalar axios/ky/ofetch |
| State management | **Svelte 5 runes** (`$state`, `$derived`) | Built-in, suficiente para 5 pantallas. NO instalar stores externos |
| Forms | **sveltekit-superforms + formsnap + zod** | Stack oficial de shadcn-svelte para forms |
| Toast | **sonner** (via shadcn-svelte) | Ya viene con el preset, solo agregar `<Toaster />` |
| Animaciones | **svelte/transition + svelte/motion** | Built-in. NO instalar framer-motion/motion |
| Charts | **layerchart** | Svelte-nativo, basado en d3, recomendado por shadcn-svelte |
| Tablas | **HTML table + shadcn `Table`** | Suficiente para datos simples. Solo usar @tanstack/svelte-table si se necesita sort/filter |
| SEO | **`<svelte:head>`** | Built-in. NO instalar svelte-meta-tags |
| i18n | **Objeto TS simple con $state** | Solo 20 keys, NO instalar librerías de i18n |
| Dark mode | **mode-watcher** (ya instalado) | Default: dark. Toggle: `import { toggleMode } from 'mode-watcher'` |
| Iconos | **phosphor-svelte** (ya instalado) | 7000+ iconos, 6 pesos. NO instalar lucide |

### API Backend

**Base URL**: `https://api.eclalune.com` (configurable via `VITE_API_URL`)

| Endpoint | Método | Descripción |
|---|---|---|
| `/price` | GET | Precio BTC verificado |
| `/score/{address}` | GET | Score de dirección Bitcoin (0-750) |
| `/simulate/volatility` | POST `{amount_usd, days_history}` | Análisis de volatilidad |
| `/simulate/conversion` | POST `{amount_usd, days_history}` | Estrategia DCA vs lump sum |
| `/remittance/compare` | POST `{amount_usd, frequency}` | Comparar canales de envío |
| `/remittance/fees` | GET | Datos de fees actuales |

> **Auth endpoints** (`/auth/challenge`, `/auth/verify`, `/auth/me`) existen pero NO se implementan en esta fase. El login será mock por ahora.

---

## Estructura de archivos objetivo

```
src/
├── app.css                           ← YA EXISTE (tema shadcn)
├── app.html                          ← YA EXISTE
├── app.d.ts                          ← YA EXISTE
├── lib/
│   ├── components/
│   │   ├── ui/                       ← shadcn (instalar con CLI, NO crear manual)
│   │   ├── score-gauge.svelte        ← gauge semicircular SVG animado
│   │   ├── breakdown-bar.svelte      ← barra de progreso horizontal
│   │   ├── btc-address-input.svelte  ← input con validación BTC
│   │   ├── channel-card.svelte       ← tarjeta de canal de remesa
│   │   ├── savings-card.svelte       ← tarjeta de ahorro anual
│   │   ├── risk-chart.svelte         ← gráfico de líneas layerchart
│   │   ├── price-ticker.svelte       ← precio BTC en vivo
│   │   └── loading-shimmer.svelte    ← skeleton loader
│   ├── api/
│   │   ├── client.ts                 ← fetch wrapper
│   │   └── endpoints.ts              ← constantes de URL
│   ├── models/
│   │   ├── score.ts
│   │   ├── price.ts
│   │   ├── simulation.ts
│   │   └── remittance.ts
│   ├── stores/
│   │   └── auth.svelte.ts            ← estado auth (mock por ahora)
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── i18n/
│   │   ├── index.ts
│   │   ├── en.ts
│   │   └── es.ts
│   ├── utils.ts                      ← YA EXISTE (shadcn cn utility)
│   └── index.ts                      ← YA EXISTE
├── routes/
│   ├── +layout.svelte                ← YA EXISTE (app.css + ModeWatcher + Toaster)
│   ├── +page.svelte                  ← redirect a /login o /home
│   ├── login/
│   │   └── +page.svelte
│   └── (app)/                        ← layout group autenticado
│       ├── +layout.svelte            ← shell: sidebar desktop + bottom nav mobile
│       ├── home/
│       │   ├── +page.svelte
│       │   └── +page.ts              ← load: fetch precio
│       ├── score/
│       │   └── +page.svelte
│       ├── simulator/
│       │   └── +page.svelte
│       └── remittance/
│           └── +page.svelte
```

---

## REGLAS OBLIGATORIAS (leer antes de cada tarea)

### Svelte 5 — Sintaxis moderna ÚNICAMENTE

```svelte
<!-- CORRECTO ✅ -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  let { title, children } = $props();
</script>

<button onclick={() => count++}>{count}</button>
{@render children()}

<!-- INCORRECTO ❌ — NUNCA usar esto -->
<script>
  let count = 0;           // ❌ no es reactivo sin $state
  $: doubled = count * 2;  // ❌ sintaxis legacy
  export let title;         // ❌ usar $props()
</script>

<button on:click={...}>    // ❌ usar onclick={}
<slot />                    // ❌ usar {@render children()}
```

### SvelteKit — Convenciones de routing

- Cada ruta es una **carpeta** en `src/routes/` con `+page.svelte`
- `+page.ts` = load function (se ejecuta antes de renderizar, datos disponibles via `data` prop)
- `+layout.svelte` = layout compartido (envuelve las páginas hijas)
- `(nombre)` = layout group (agrupa rutas sin afectar la URL)
- `goto('/ruta')` para navegación programática, `<a href="/ruta">` para links

### shadcn-svelte — Cómo usar componentes

```bash
# Instalar un componente (SIEMPRE con CLI, NUNCA copiar manualmente):
bun x shadcn-svelte@latest add button

# Usar en un .svelte:
import { Button } from '$lib/components/ui/button';
```

### Tailwind — Clases de shadcn disponibles

```
bg-background, bg-card, bg-popover, bg-primary, bg-secondary, bg-muted, bg-accent, bg-destructive
text-foreground, text-card-foreground, text-muted-foreground, text-primary-foreground
border-border, border-input
rounded-sm, rounded-md, rounded-lg, rounded-xl
```

### Phosphor icons — Cómo importar

```svelte
<script>
  import SquaresFour from 'phosphor-svelte/lib/SquaresFour';
  import ChartBar from 'phosphor-svelte/lib/ChartBar';
</script>

<SquaresFour size={24} weight="bold" />
```

---

## TAREA 0 — Instalar dependencias

**Ejecutar estos comandos exactos en orden:**

```bash
cd C:\Users\wilme\OneDrive\Escritorio\CUBO\front-end-svelte

# 1. Componentes shadcn-svelte
bun x shadcn-svelte@latest add button card input label badge alert separator skeleton table select sheet dialog sonner

# 2. Forms (stack oficial shadcn-svelte)
bun add sveltekit-superforms formsnap zod

# 3. Charts
bun add layerchart d3-scale d3-shape

# 4. Verificar que compila
bun run build
```

Si `bun run build` falla, corregir antes de seguir.

---

## TAREA 1 — Modelos TypeScript

Crear 4 archivos. Solo `interface`, sin clases, sin decoradores.

**Archivo: `src/lib/models/price.ts`**
```ts
export interface VerifiedPrice {
  price_usd: number;
  sources_count: number;
  deviation: number;
  has_warning: boolean;
}
```

**Archivo: `src/lib/models/score.ts`**
```ts
export interface ScoreBreakdown {
  consistency: number;
  relative_volume: number;
  diversification: number;
  savings_pattern: number;
  payment_history: number;
  lightning_activity: number;
}

export interface ScoreResult {
  total_score: number;
  rank: 'Excellent' | 'Good' | 'Fair' | 'Developing' | 'New';
  address: string;
  breakdown: ScoreBreakdown;
  recommendations: string[];
}
```

**Archivo: `src/lib/models/simulation.ts`**
```ts
export interface DayAnalysis {
  wait_days: number;
  avg_return: number;
  std_dev: number;
  worst_case: number;
  best_case: number;
  risk_zone: 'low' | 'medium' | 'high';
}

export interface SimulationResult {
  daily_analysis: DayAnalysis[];
  recommendation: string;
  risk_level: string;
  optimal_day: number;
  expected_return: number;
}

export interface PurchaseStrategy {
  amount: number;
  risk: number;
  sharpe_ratio: number;
}

export interface DcaStrategy {
  amount_per_period: number;
  periods: number;
  risk: number;
}

export interface ConversionResult {
  strategy: string;
  explanation: string;
  lump_sum: PurchaseStrategy;
  dca: DcaStrategy;
}
```

**Archivo: `src/lib/models/remittance.ts`**
```ts
export interface ChannelComparison {
  name: 'Lightning' | 'On-chain' | 'Traditional';
  fee_percent: number;
  fee_usd: number;
  amount_received: number;
  estimated_time: string;
  is_recommended: boolean;
}

export interface SendTimeRecommendation {
  best_time: string;
  current_fee_sat_vb: number;
  estimated_low_fee_sat_vb: number;
  savings_percent: number;
}

export interface RemittanceResult {
  channels: ChannelComparison[];
  annual_savings: number;
  best_channel: string;
  best_time?: SendTimeRecommendation;
}
```

**Verificar:** `bun run build`

---

## TAREA 2 — Cliente API

Wrapper mínimo sobre `fetch` nativo. NO instalar axios, ky, ofetch ni ningún otro HTTP client.

**Archivo: `src/lib/api/endpoints.ts`**
```ts
const BASE_URL = import.meta.env.VITE_API_URL ?? 'https://api.eclalune.com';

export const endpoints = {
  price: `${BASE_URL}/price`,
  score: (address: string) => `${BASE_URL}/score/${address}`,
  simulate: {
    volatility: `${BASE_URL}/simulate/volatility`,
    conversion: `${BASE_URL}/simulate/conversion`,
  },
  remittance: {
    compare: `${BASE_URL}/remittance/compare`,
    fees: `${BASE_URL}/remittance/fees`,
  },
} as const;
```

**Archivo: `src/lib/api/client.ts`**
```ts
class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  const res = await fetch(url, { ...options, headers });

  if (!res.ok) {
    throw new ApiError(res.status, await res.text());
  }

  return res.json();
}

export const api = {
  get: <T>(url: string) => request<T>(url),
  post: <T>(url: string, body: unknown) =>
    request<T>(url, { method: 'POST', body: JSON.stringify(body) }),
};
```

> **Sin auth por ahora.** Cuando se implemente Nostr, se agrega el header `Authorization` aquí.

**Verificar:** `bun run build`

---

## TAREA 3 — Auth Store (mock)

Auth mock para poder navegar. Se reemplazará con Nostr después.

**Archivo: `src/lib/stores/auth.svelte.ts`**
```ts
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
```

**Verificar:** `bun run build`

---

## TAREA 4 — Utilidades

**Archivo: `src/lib/utils/formatters.ts`**
```ts
export function formatUSD(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

export function formatBTC(value: number): string {
  return `₿ ${value.toFixed(8)}`;
}

export function formatPercent(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

export function formatSatVb(value: number): string {
  return `${value} sat/vB`;
}
```

**Archivo: `src/lib/utils/validators.ts`**
```ts
export function isValidBtcAddress(address: string): boolean {
  return /^(bc1q[a-z0-9]{38,58}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$/.test(address);
}
```

**Verificar:** `bun run build`

---

## TAREA 5 — i18n simple

Solo un objeto TS con `$state` para el locale. NO instalar librerías de i18n.

**Archivo: `src/lib/i18n/en.ts`**
```ts
export const en = {
  nav: { home: 'Home', score: 'Score', simulator: 'Simulator', remittance: 'Remittance', logout: 'Logout' },
  home: {
    welcome: 'Bitcoin Financial Intelligence',
    quickActions: 'Quick Actions',
    analyzeAddress: 'Analyze Address',
    volatilitySimulator: 'Volatility Simulator',
    remittanceOptimizer: 'Remittance Optimizer',
    dontTrust: "Don't trust, verify",
  },
  price: { fromSources: 'from {count} sources', verified: 'Verified' },
  score: {
    title: 'Bitcoin Score',
    enterAddress: 'Enter a Bitcoin address to analyze',
    verify: 'Verify',
    recommendations: 'Recommendations',
  },
  simulator: {
    title: 'Volatility Simulator',
    amount: 'Amount (USD)',
    period: 'Analysis Period',
    run: 'Run Simulation',
    optimalDay: 'Optimal Day',
    expectedReturn: 'Expected Return',
    riskLevel: 'Risk Level',
    recommendation: 'Recommendation',
  },
  remittance: {
    title: 'Remittance Optimizer',
    amount: 'Amount (USD)',
    frequency: 'Frequency',
    compare: 'Compare Channels',
    annualSavings: 'Annual Savings',
    bestTime: 'Best Time to Send',
    recommended: 'Recommended',
  },
  common: { loading: 'Loading...', error: 'Error', retry: 'Retry', cancel: 'Cancel', close: 'Close' },
} as const;

export type Translations = typeof en;
```

**Archivo: `src/lib/i18n/es.ts`**
```ts
import type { Translations } from './en';

export const es: Translations = {
  nav: { home: 'Inicio', score: 'Score', simulator: 'Simulador', remittance: 'Remesas', logout: 'Salir' },
  home: {
    welcome: 'Inteligencia Financiera Bitcoin',
    quickActions: 'Acciones Rápidas',
    analyzeAddress: 'Analizar Dirección',
    volatilitySimulator: 'Simulador de Volatilidad',
    remittanceOptimizer: 'Optimizador de Remesas',
    dontTrust: 'No confíes, verifica',
  },
  price: { fromSources: 'de {count} fuentes', verified: 'Verificado' },
  score: {
    title: 'Score Bitcoin',
    enterAddress: 'Ingresa una dirección Bitcoin para analizar',
    verify: 'Verificar',
    recommendations: 'Recomendaciones',
  },
  simulator: {
    title: 'Simulador de Volatilidad',
    amount: 'Monto (USD)',
    period: 'Período de Análisis',
    run: 'Ejecutar Simulación',
    optimalDay: 'Día Óptimo',
    expectedReturn: 'Retorno Esperado',
    riskLevel: 'Nivel de Riesgo',
    recommendation: 'Recomendación',
  },
  remittance: {
    title: 'Optimizador de Remesas',
    amount: 'Monto (USD)',
    frequency: 'Frecuencia',
    compare: 'Comparar Canales',
    annualSavings: 'Ahorro Anual',
    bestTime: 'Mejor Momento para Enviar',
    recommended: 'Recomendado',
  },
  common: { loading: 'Cargando...', error: 'Error', retry: 'Reintentar', cancel: 'Cancelar', close: 'Cerrar' },
};
```

**Archivo: `src/lib/i18n/index.ts`**

> **IMPORTANTE**: este archivo DEBE tener extensión `.svelte.ts` para que `$state` funcione.
> Renombrar a `src/lib/i18n/index.svelte.ts`

```ts
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
```

**Uso en componentes:**
```svelte
<script lang="ts">
  import { i18n } from '$lib/i18n/index.svelte';
</script>

<h1>{i18n.t.home.welcome}</h1>
```

**Verificar:** `bun run build`

---

## TAREA 6 — Layout raíz (actualizar el existente)

Actualizar `src/routes/+layout.svelte` (YA EXISTE) para agregar Toaster.

```svelte
<script lang="ts">
  import '../app.css';
  import { ModeWatcher } from 'mode-watcher';
  import { Toaster } from '$lib/components/ui/sonner';
  import favicon from '$lib/assets/favicon.svg';

  let { children } = $props();
</script>

<ModeWatcher defaultMode="dark" />
<Toaster />

<svelte:head>
  <link rel="icon" href={favicon} />
  <title>Magma</title>
</svelte:head>

{@render children()}
```

> **NOTA**: `ModeWatcher` ya está en el archivo actual. Solo agregar `Toaster` y `<title>`.

**Verificar:** `bun run build`

---

## TAREA 7 — Routing: página raíz + auth guard

**Archivo: `src/routes/+page.svelte`** (reemplazar el existente)
```svelte
<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { auth } from '$lib/stores/auth.svelte';

  if (browser) {
    goto(auth.isAuthenticated ? '/home' : '/login', { replaceState: true });
  }
</script>
```

**Archivo: `src/routes/(app)/+layout.svelte`** (crear)

Este es el shell para todas las rutas autenticadas. Sidebar en desktop, bottom nav en mobile.

```svelte
<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { auth } from '$lib/stores/auth.svelte';
  import { browser } from '$app/environment';
  import { i18n } from '$lib/i18n/index.svelte';
  import { Button } from '$lib/components/ui/button';
  import { Separator } from '$lib/components/ui/separator';
  import { toggleMode } from 'mode-watcher';
  import SquaresFour from 'phosphor-svelte/lib/SquaresFour';
  import ChartBar from 'phosphor-svelte/lib/ChartBar';
  import TrendUp from 'phosphor-svelte/lib/TrendUp';
  import ArrowsLeftRight from 'phosphor-svelte/lib/ArrowsLeftRight';
  import SignOut from 'phosphor-svelte/lib/SignOut';
  import Moon from 'phosphor-svelte/lib/Moon';
  import Sun from 'phosphor-svelte/lib/Sun';

  let { children } = $props();

  // Redirect si no autenticado
  if (browser && !auth.isAuthenticated) {
    goto('/login', { replaceState: true });
  }

  const navItems = [
    { href: '/home', icon: SquaresFour, label: i18n.t.nav.home },
    { href: '/score', icon: ChartBar, label: i18n.t.nav.score },
    { href: '/simulator', icon: TrendUp, label: i18n.t.nav.simulator },
    { href: '/remittance', icon: ArrowsLeftRight, label: i18n.t.nav.remittance },
  ];

  let currentPath = $derived(page.url.pathname);

  function handleLogout() {
    auth.logout();
    goto('/login');
  }
</script>

<!-- DESKTOP: sidebar + content -->
<div class="flex h-screen">
  <aside class="hidden lg:flex w-60 flex-col border-r border-sidebar-border bg-sidebar p-4">
    <!-- Logo -->
    <div class="mb-8 px-2">
      <h1 class="font-heading text-xl font-bold text-sidebar-foreground">Magma</h1>
      <p class="text-xs text-sidebar-foreground/60">Bitcoin Financial Intelligence</p>
    </div>

    <!-- Nav items -->
    <nav class="flex flex-1 flex-col gap-1">
      {#each navItems as item}
        <a
          href={item.href}
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors
            {currentPath === item.href
              ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium'
              : 'text-sidebar-foreground/60 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground'}"
        >
          <item.icon size={20} weight={currentPath === item.href ? 'fill' : 'regular'} />
          {item.label}
        </a>
      {/each}
    </nav>

    <Separator class="my-2" />

    <!-- Bottom actions -->
    <div class="flex flex-col gap-1">
      <Button variant="ghost" size="sm" class="justify-start gap-3" onclick={toggleMode}>
        <Sun size={18} class="dark:hidden" />
        <Moon size={18} class="hidden dark:block" />
        Theme
      </Button>
      <Button variant="ghost" size="sm" class="justify-start gap-3 text-destructive" onclick={handleLogout}>
        <SignOut size={18} />
        {i18n.t.nav.logout}
      </Button>
    </div>
  </aside>

  <!-- Content area -->
  <main class="flex-1 overflow-y-auto pb-20 lg:pb-0">
    <div class="mx-auto max-w-5xl p-4 lg:p-6">
      {@render children()}
    </div>
  </main>
</div>

<!-- MOBILE: bottom nav -->
<nav class="fixed inset-x-0 bottom-0 z-50 flex items-center justify-around border-t border-border bg-background p-2 lg:hidden">
  {#each navItems as item}
    <a
      href={item.href}
      class="flex flex-col items-center gap-0.5 px-3 py-1 text-xs transition-colors
        {currentPath === item.href
          ? 'text-primary font-medium'
          : 'text-muted-foreground'}"
    >
      <item.icon size={22} weight={currentPath === item.href ? 'fill' : 'regular'} />
      {item.label}
    </a>
  {/each}
</nav>
```

**Verificar:** `bun run build`

---

## TAREA 8 — Login

**Archivo: `src/routes/login/+page.svelte`**

Login mock (sin Nostr). El usuario hace click en "Connect" y entra.

**Diseño**:
- Desktop: 2 columnas (branding izq, form der)
- Mobile: stacked (branding arriba, form abajo)

**Componentes shadcn a usar**: `Card`, `Input`, `Button`, `Label`

**Elementos**:
- Logo "Magma" + tagline "Bitcoin Financial Intelligence"
- Input de texto (placeholder: "nsec1... or hex private key") — solo visual, no valida
- Botón "Connect" → llama `auth.login()` → `goto('/home')`
- Texto footer: "Your keys never leave your device" con icono Lock
- Estilo: Card centrada con fondo sutil, borde suave

```svelte
<script lang="ts">
  import { goto } from '$app/navigation';
  import { auth } from '$lib/stores/auth.svelte';
  import { Button } from '$lib/components/ui/button';
  import { Card } from '$lib/components/ui/card';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import Lock from 'phosphor-svelte/lib/Lock';
  import Lightning from 'phosphor-svelte/lib/Lightning';

  let key = $state('');

  function handleConnect() {
    auth.login();
    goto('/home');
  }
</script>

<!-- Implementar el layout 2 columnas / stacked aquí -->
```

> Al implementador: diseñar con buen gusto usando las clases de Tailwind/shadcn. Referencia visual: card centrada estilo login de apps fintech modernas. El branding usa colores `primary` (naranja quemado) del tema.

**Verificar:** `bun run build` y navegar a `/login`

---

## TAREA 9 — Home / Dashboard

**Archivo: `src/routes/(app)/home/+page.ts`** (load function)
```ts
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
```

**Archivo: `src/routes/(app)/home/+page.svelte`**

**Elementos**:
1. **Hero**: precio BTC/USD grande con `Skeleton` mientras carga. Fuentes count + badge "Verified"
2. **Grid 3 cards** (tool cards): Score, Simulator, Remittance — cada una con icono, título, descripción corta, link `<a href="/score">`
3. **Welcome card**: texto de bienvenida + features lista + badge "Don't trust, verify"

**Componentes shadcn**: `Card`, `Badge`, `Button`, `Skeleton`

```svelte
<script lang="ts">
  import type { VerifiedPrice } from '$lib/models/price';
  import { formatUSD } from '$lib/utils/formatters';
  import { i18n } from '$lib/i18n/index.svelte';
  import { Card } from '$lib/components/ui/card';
  import { Badge } from '$lib/components/ui/badge';
  import { Skeleton } from '$lib/components/ui/skeleton';
  import ChartBar from 'phosphor-svelte/lib/ChartBar';
  import TrendUp from 'phosphor-svelte/lib/TrendUp';
  import ArrowsLeftRight from 'phosphor-svelte/lib/ArrowsLeftRight';

  let { data } = $props<{ data: { price: VerifiedPrice | null } }>();
</script>

<!-- Implementar hero + grid + welcome -->
```

**Verificar:** `bun run build` y navegar a `/home`

---

## TAREA 10 — Score Screen

**Archivo: `src/routes/(app)/score/+page.svelte`**

Sin load function — es interactivo.

**Estado local:**
```ts
let address = $state('');
let result = $state<ScoreResult | null>(null);
let isLoading = $state(false);
let error = $state<string | null>(null);
```

**Flujo**: input → fetch `/score/{address}` → mostrar resultado

**Sub-componentes a crear:**

### `src/lib/components/score-gauge.svelte`
- SVG semicírculo (arco de 180°)
- Props: `score: number` (0-750), `rank: string`
- Animación: CSS transition en `stroke-dashoffset`
- Color del arco: verde (#22c55e) si >600, naranja (#f97316) si >400, amarillo (#eab308) si >200, rojo (#ef4444) si <200
- Centro: número de score grande + rank badge debajo

### `src/lib/components/breakdown-bar.svelte`
- Props: `label: string`, `score: number`, `maxScore: number`
- Barra horizontal con div interior proporcional
- Color: verde (>80%), naranja (>50%), amarillo (<50%)
- Label a la izquierda, "score/maxScore" a la derecha

**Componentes shadcn**: `Card`, `Input`, `Button`, `Badge`, `Alert`, `Skeleton`

**Verificar:** `bun run build`

---

## TAREA 11 — Simulator Screen

**Archivo: `src/routes/(app)/simulator/+page.svelte`**

**Estado local:**
```ts
let amountUsd = $state(100);
let daysHistory = $state(30);
let result = $state<SimulationResult | null>(null);
let isLoading = $state(false);
let error = $state<string | null>(null);
```

**Flujo**: inputs → fetch POST `/simulate/volatility` → mostrar resultado

**Elementos del resultado:**
1. Card de recomendación (texto + badge de risk level)
2. 3 stat badges inline: Optimal Day, Expected Return, Risk Level
3. **Risk chart** (crear `src/lib/components/risk-chart.svelte`)
4. Tabla de datos con shadcn `Table`

### `src/lib/components/risk-chart.svelte`
- Usar `layerchart`: `Chart`, `Svg`, `Line`, `Axis`, `Tooltip`
- Props: `data: DayAnalysis[]`
- 3 líneas:
  - `avg_return` → color primary (naranja), stroke sólido
  - `best_case` → color verde, stroke punteado
  - `worst_case` → color rojo, stroke punteado
- Eje X: `wait_days` (días)
- Eje Y: return %

**Componentes shadcn**: `Card`, `Input`, `Button`, `Badge`, `Select`, `Table`, `Skeleton`

**Verificar:** `bun run build`

---

## TAREA 12 — Remittance Screen

**Archivo: `src/routes/(app)/remittance/+page.svelte`**

**Estado local:**
```ts
let amountUsd = $state(200);
let frequency = $state<'monthly' | 'biweekly' | 'weekly'>('monthly');
let result = $state<RemittanceResult | null>(null);
let isLoading = $state(false);
let error = $state<string | null>(null);
```

**Flujo**: inputs → fetch POST `/remittance/compare` → mostrar resultado

**Sub-componentes:**

### `src/lib/components/channel-card.svelte`
- Props: `channel: ChannelComparison`
- Card de shadcn. Si `is_recommended`: borde izquierdo primary + badge "RECOMMENDED"
- Contenido: nombre, fee%, monto recibido (formatUSD), tiempo estimado

### `src/lib/components/savings-card.svelte`
- Props: `annualSavings: number`, `bestChannel: string`
- Card destacada con monto grande en verde + "vs worst channel" + monto mensual

**Elementos adicionales:**
- Si `best_time` existe: card con mejor hora, fee actual vs baja, % ahorro

**Componentes shadcn**: `Card`, `Input`, `Button`, `Badge`, `Select`, `Skeleton`

**Verificar:** `bun run build`

---

## Orden de ejecución

```
TAREA 0  → Instalar deps
TAREA 1  → Modelos TS         ⎤
TAREA 2  → API client          ⎥ Paralelizables
TAREA 3  → Auth store (mock)   ⎥
TAREA 4  → Utilidades          ⎥
TAREA 5  → i18n               ⎦
TAREA 6  → Layout raíz (actualizar)
TAREA 7  → Routing + auth guard + layout (app)
TAREA 8  → Login
TAREA 9  → Home
TAREA 10 → Score + gauge + breakdown
TAREA 11 → Simulator + risk chart
TAREA 12 → Remittance + channel card + savings card
```

## Verificación final

```bash
bun run build       # Sin errores
bun run dev         # Abrir en navegador
```

Probar: `/login` → click Connect → `/home` → navegar a cada sección → logout → vuelve a `/login`.
