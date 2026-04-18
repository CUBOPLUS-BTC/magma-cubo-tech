<script lang="ts">
  import type { VerifiedPrice } from '$lib/models/price';
  import type { NetworkStatus } from '$lib/models/network';
  import type { AchievementsResponse } from '$lib/models/achievements';
  import { formatUSD } from '$lib/utils/formatters';
  import { i18n } from '$lib/i18n/index.svelte';
  import { resolve } from '$app/paths';
  import { api } from '$lib/api/client';
  import { endpoints } from '$lib/api/endpoints';
  import { Badge } from '$lib/components/ui/badge';
  import { Skeleton } from '$lib/components/ui/skeleton';
  import { Card, CardContent } from '$lib/components/ui/card';
  import { Input } from '$lib/components/ui/input';
  import { Button } from '$lib/components/ui/button';
  import PaperPlaneTilt from 'phosphor-svelte/lib/PaperPlaneTilt';
  import PiggyBank from 'phosphor-svelte/lib/PiggyBank';
  import CurrencyBtc from 'phosphor-svelte/lib/CurrencyBtc';
  import Lightning from 'phosphor-svelte/lib/Lightning';
  import Cube from 'phosphor-svelte/lib/Cube';
  import ArrowRight from 'phosphor-svelte/lib/ArrowRight';
  import ArrowsLeftRight from 'phosphor-svelte/lib/ArrowsLeftRight';
  import Trophy from 'phosphor-svelte/lib/Trophy';
  import Medal from 'phosphor-svelte/lib/Medal';
  import Star from 'phosphor-svelte/lib/Star';
  import Fire from 'phosphor-svelte/lib/Fire';
  import Geo from '$lib/components/geo.svelte';
  import { browser } from '$app/environment';
  import { alertStore } from '$lib/stores/alerts.svelte';
  import AlertBanner from '$lib/components/alert-banner.svelte';
  import { onDestroy } from 'svelte';

  let { data }: { data: { price: VerifiedPrice | null; network: NetworkStatus | null } } = $props();

  let calcUsd = $state(100);
  let calcBtc = $derived(
    data.price && data.price.price_usd > 0
      ? (calcUsd / data.price.price_usd)
      : 0
  );

  let onboarded = $state(browser ? !!localStorage.getItem('magma_onboarded') : true);
  let achievements = $state<AchievementsResponse | null>(null);

  $effect(() => {
    api.get<AchievementsResponse>(endpoints.achievements)
      .then((res) => { achievements = res; })
      .catch(() => {});
  });

  const tools = $derived([
    {
      icon: PaperPlaneTilt,
      title: () => i18n.t.home.tools.remittance.title,
      description: () => i18n.t.home.tools.remittance.description,
      href: '/remittance',
    },
    {
      icon: PiggyBank,
      title: () => i18n.t.home.tools.pension.title,
      description: () => i18n.t.home.tools.pension.description,
      href: '/pension',
    },
    {
      icon: CurrencyBtc,
      title: () => i18n.t.home.tools.savings.title,
      description: () => i18n.t.home.tools.savings.description,
      href: '/savings',
    },
  ]);

  $effect(() => {
    alertStore.startPolling();
  });

  onDestroy(() => {
    alertStore.stopPolling();
  });
</script>

<svelte:head>
  <title>{i18n.t.nav.home} {i18n.t.app.titleSuffix}</title>
</svelte:head>

<div class="space-y-8">
  {#if !onboarded}
    <Card class="border-primary/20 bg-primary/5">
      <CardContent class="pt-6 space-y-4">
        <div class="flex items-center gap-3">
          <Geo state="success" class="w-12 h-12 shrink-0" />
          <div>
            <h2 class="font-heading text-lg font-semibold">Welcome to Magma!</h2>
            <p class="text-sm text-muted-foreground">Your Bitcoin financial toolkit</p>
          </div>
        </div>
        <ol class="space-y-2 text-sm text-muted-foreground list-decimal list-inside">
          <li>Check real-time BTC price from multiple sources</li>
          <li>Compare remittance fees and find the best time to send</li>
          <li>Start your Bitcoin savings journey with DCA projections</li>
        </ol>
        <Button size="sm" onclick={() => { localStorage.setItem('magma_onboarded', '1'); onboarded = true; }}>
          Got it!
        </Button>
      </CardContent>
    </Card>
  {/if}

  <section class="pt-2">
    {#if data.price}
      <div class="flex items-start gap-4">
        <Geo state="idle" class="w-20 h-20 shrink-0 hidden sm:block" />
        <div class="space-y-1">
          <span class="text-sm font-medium text-muted-foreground uppercase tracking-wider">BTC/USD</span>
          <div class="flex items-baseline gap-3">
            <span class="font-heading text-5xl sm:text-6xl font-bold text-foreground tabular-nums tracking-tight">
              {formatUSD(data.price.price_usd)}
            </span>
          </div>
          <div class="flex gap-2 pt-1">
            <Badge variant="secondary" class="text-xs font-normal">
              {i18n.t.home.sources.replace('{count}', String(data.price.sources_count))}
            </Badge>
            <Badge variant="default" class="text-xs font-normal">{i18n.t.home.verified}</Badge>
          </div>
        </div>
      </div>
    {:else}
      <div class="space-y-2">
        <Skeleton class="h-4 w-16" />
        <Skeleton class="h-14 w-64" />
        <Skeleton class="h-5 w-32" />
      </div>
    {/if}
  </section>

  <AlertBanner status={alertStore.status} />

  <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <Card>
      <CardContent class="pt-6 space-y-4">
        <div class="flex items-center gap-2 text-sm font-medium text-muted-foreground">
          <ArrowsLeftRight size={18} />
          {i18n.t.home.calculator}
        </div>
        <div class="space-y-3">
          <div class="flex items-center gap-2">
            <Input
              type="number"
              bind:value={calcUsd}
              min="0"
              step="1"
              class="tabular-nums"
            />
            <span class="text-sm font-medium text-muted-foreground shrink-0">USD</span>
          </div>
          <div class="text-2xl font-bold text-primary tabular-nums">
            = {calcBtc.toFixed(8)} BTC
          </div>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardContent class="pt-6 space-y-4">
        <div class="flex items-center gap-2 text-sm font-medium text-muted-foreground">
          <Cube size={18} />
          {i18n.t.home.networkStatus}
        </div>
        {#if data.network}
          <div class="space-y-2.5">
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">{i18n.t.home.blockHeight}</span>
              <span class="text-sm font-semibold tabular-nums">#{data.network.block_height.toLocaleString()}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">{i18n.t.home.fastFee}</span>
              <span class="text-sm font-semibold tabular-nums">{data.network.fees.fastestFee} sat/vB</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">{i18n.t.home.economyFee}</span>
              <span class="text-sm font-semibold tabular-nums text-green-600 dark:text-green-500">{data.network.fees.economyFee} sat/vB</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-muted-foreground">{i18n.t.home.mempoolTxs}</span>
              <span class="text-sm font-semibold tabular-nums">{data.network.mempool_size.count.toLocaleString()} txs</span>
            </div>
          </div>
        {:else}
          <div class="space-y-2">
            <Skeleton class="h-5 w-full" />
            <Skeleton class="h-5 w-full" />
            <Skeleton class="h-5 w-full" />
          </div>
        {/if}
      </CardContent>
    </Card>
  </section>

  <section>
    <h2 class="font-heading text-lg font-semibold mb-4">{i18n.t.home.toolsTitle}</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {#each tools as tool (tool.href)}
        <a
          href={resolve(tool.href as '/remittance' | '/pension' | '/savings')}
          class="group block"
        >
          <Card class="p-5 h-full transition-all hover:border-primary/30 hover:shadow-md active:scale-[0.98]">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <tool.icon size={24} class="text-primary" weight="regular" />
                <ArrowRight size={18} class="text-muted-foreground/40 transition-transform group-hover:translate-x-0.5 group-hover:text-primary" weight="bold" />
              </div>
              <div class="space-y-1">
                <h3 class="font-heading text-base font-semibold text-foreground">{tool.title()}</h3>
                <p class="text-sm text-muted-foreground leading-relaxed">{tool.description()}</p>
              </div>
            </div>
          </Card>
        </a>
      {/each}
    </div>
  </section>

  <section>
    <div class="flex items-center justify-between mb-4">
      <h2 class="font-heading text-lg font-semibold">{i18n.t.achievements.title}</h2>
      {#if achievements}
        <Badge variant="secondary">{i18n.t.achievements.level} {achievements.level}</Badge>
      {/if}
    </div>

    {#if achievements}
      <div class="mb-4">
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-sm text-muted-foreground">{i18n.t.achievements.progress}</span>
          <span class="text-sm font-medium tabular-nums">{achievements.total_xp} XP</span>
        </div>
        <div class="h-2 rounded-full bg-muted overflow-hidden">
          <div
            class="h-full rounded-full bg-primary transition-all"
            style="width: {achievements.next_level_xp ? Math.min((achievements.total_xp / achievements.next_level_xp) * 100, 100) : 100}%"
          ></div>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {#each achievements.achievements as achievement (achievement.id)}
          <div
            class="rounded-xl border p-4 text-center transition-all {achievement.earned ? 'border-primary/40 bg-primary/5' : 'border-border opacity-40'}"
          >
            <div class="flex justify-center mb-2">
              {#if achievement.earned}
                <Trophy size={24} class="text-primary" weight="fill" />
              {:else}
                <Medal size={24} class="text-muted-foreground" weight="regular" />
              {/if}
            </div>
            <p class="text-sm font-medium text-foreground">{achievement.name}</p>
            <p class="text-xs text-muted-foreground mt-0.5">{achievement.xp} {i18n.t.achievements.xp}</p>
          </div>
        {/each}
      </div>
    {:else}
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {#each Array(6) as _, i}
          <div class="rounded-xl border border-border p-4 text-center">
            <div class="flex justify-center mb-2">
              <Skeleton class="h-6 w-6 rounded-full" />
            </div>
            <Skeleton class="h-4 w-20 mx-auto mb-1" />
            <Skeleton class="h-3 w-12 mx-auto" />
          </div>
        {/each}
      </div>
    {/if}
  </section>
</div>
