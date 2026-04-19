<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';
  import { auth } from '$lib/stores/auth.svelte';
  import { i18n } from '$lib/i18n/index.svelte';
  import { Button } from '$lib/components/ui/button';
  import { Separator } from '$lib/components/ui/separator';
  import Flame from 'phosphor-svelte/lib/Flame';
  import Mountains from 'phosphor-svelte/lib/Mountains';
  import PaperPlaneTilt from 'phosphor-svelte/lib/PaperPlaneTilt';
  import PiggyBank from 'phosphor-svelte/lib/PiggyBank';
  import CurrencyBtc from 'phosphor-svelte/lib/CurrencyBtc';
  import Door from 'phosphor-svelte/lib/Door';
  import UserCircle from 'phosphor-svelte/lib/UserCircle';

  let { children } = $props();

  $effect(() => {
    if (!auth.isAuthenticated) {
      goto(resolve('/login'), { replaceState: true });
    }
  });

  const navItems = $derived([
    { href: '/home', icon: Flame, label: i18n.t.nav.home },
    { href: '/remittance', icon: PaperPlaneTilt, label: i18n.t.nav.remittance },
    { href: '/pension', icon: PiggyBank, label: i18n.t.nav.pension },
    { href: '/savings', icon: CurrencyBtc, label: i18n.t.nav.savings },
  ]);

  let currentPath = $derived(page.url.pathname);

  function handleLogout() {
    auth.logout();
    goto(resolve('/login'));
  }
</script>

<div class="flex h-screen">
  <aside class="hidden lg:flex w-56 flex-col border-r border-sidebar-border bg-sidebar px-3 py-5">
    <div class="mb-6 px-3">
      <div class="flex items-center gap-2.5">
        <Mountains class="size-7 text-primary" weight="bold" />
        <h1 class="font-heading text-lg font-semibold text-sidebar-foreground tracking-tight">{i18n.t.app.name}</h1>
      </div>
      <p class="text-[11px] text-muted-foreground mt-1 px-0.5">{i18n.t.app.tagline}</p>
    </div>

    <nav class="flex flex-1 flex-col gap-0.5">
      {#each navItems as item (item.href)}
        <a
          href={resolve(item.href as '/home' | '/remittance' | '/pension' | '/savings')}
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors duration-200
            {currentPath === item.href
              ? 'bg-muted text-primary font-semibold'
              : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
        >
          <item.icon size={20} weight={currentPath === item.href ? 'fill' : 'regular'} />
          {item.label}
        </a>
      {/each}
    </nav>

    <Separator class="my-3" />

    <div class="flex flex-col gap-0.5">
      <a
        href={resolve('/profile')}
        class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors duration-200
          {currentPath === '/profile'
            ? 'bg-muted text-primary font-semibold'
            : 'text-muted-foreground hover:bg-muted hover:text-foreground'}"
      >
        <UserCircle size={20} weight={currentPath === '/profile' ? 'fill' : 'regular'} />
        {i18n.t.nav.profile}
      </a>
      <Button variant="ghost" size="sm" class="justify-start gap-3 rounded-xl text-muted-foreground hover:text-red-500" onclick={handleLogout}>
        <Door size={18} />
        {i18n.t.nav.logout}
      </Button>
    </div>
  </aside>

  <main class="flex-1 overflow-y-auto pb-20 lg:pb-0 bg-background">
    <div class="mx-auto max-w-5xl px-4 py-5 lg:px-8 lg:py-6">
      {@render children()}
    </div>
  </main>
</div>

<nav class="fixed inset-x-0 bottom-0 z-50 flex items-center justify-around border-t border-border bg-card backdrop-blur-sm px-2 py-2.5 lg:hidden">
  {#each navItems as item (item.href)}
    <a
      href={resolve(item.href as '/home' | '/remittance' | '/pension' | '/savings')}
      class="flex flex-col items-center gap-1 px-3 py-1.5 text-[11px] transition-colors duration-200 rounded-xl
        {currentPath === item.href
          ? 'text-primary font-semibold'
          : 'text-muted-foreground'}"
    >
      <item.icon size={22} weight={currentPath === item.href ? 'fill' : 'regular'} />
      {item.label}
    </a>
  {/each}
  <a
    href={resolve('/profile')}
    class="flex flex-col items-center gap-1 px-3 py-1.5 text-[11px] transition-colors duration-200 rounded-xl
      {currentPath === '/profile'
        ? 'text-primary font-semibold'
        : 'text-muted-foreground'}"
  >
    <UserCircle size={22} weight={currentPath === '/profile' ? 'fill' : 'regular'} />
    {i18n.t.nav.profile}
  </a>
</nav>
