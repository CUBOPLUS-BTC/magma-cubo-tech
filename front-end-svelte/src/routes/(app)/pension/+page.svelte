<script lang="ts">
	import type { PensionProjection } from '$lib/models/pension';
	import { api } from '$lib/api/client';
	import { endpoints } from '$lib/api/endpoints';
	import { i18n } from '$lib/i18n/index.svelte';
	import { formatUSD } from '$lib/utils/formatters';
	import { createQuery } from '@tanstack/svelte-query';
	import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import PiggyBank from 'phosphor-svelte/lib/PiggyBank';
	import CurrencyBtc from 'phosphor-svelte/lib/CurrencyBtc';
	import TrendUp from 'phosphor-svelte/lib/TrendUp';
	import Geo from '$lib/components/geo.svelte';
	import SavingsChart from '$lib/components/savings-chart.svelte';
	import AnimatedNumber from '$lib/components/animated-number.svelte';
	import { animateIn, staggerChildren, pressScale } from '$lib/motion';

	let monthlySaving = $state(20);
	let years = $state(20);

	let queryInput = $state<{ monthly_saving_usd: number; years: number } | null>(null);

	const pensionQuery = createQuery(() => ({
		queryKey: ['pension-projection', queryInput] as const,
		queryFn: () => api.post<PensionProjection>(endpoints.pension.projection, queryInput!),
		enabled: queryInput !== null,
	}));

	function handleCalculate() {
		queryInput = { monthly_saving_usd: monthlySaving, years };
	}

	let result = $derived(pensionQuery.data ?? null);
	let isLoading = $derived(pensionQuery.isFetching);
	let error = $derived(pensionQuery.error?.message ?? null);
</script>

<svelte:head>
	<title>{i18n.t.pension.title} {i18n.t.app.titleSuffix}</title>
</svelte:head>

<div class="space-y-8" use:staggerChildren={{ y: 20, staggerDelay: 0.08 }}>
	<div>
		<h1 class="font-heading text-2xl font-bold tracking-tight">{i18n.t.pension.title}</h1>
		<p class="text-sm text-muted-foreground mt-1">{i18n.t.pension.subtitle}</p>
	</div>

	<Card>
		<CardHeader>
			<CardTitle class="font-heading flex items-center gap-2">
				<PiggyBank size={20} class="text-emerald-500" />
				{i18n.t.pension.formTitle}
			</CardTitle>
		</CardHeader>
		<CardContent class="space-y-6">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div class="space-y-2">
					<label for="monthly" class="text-sm font-semibold">{i18n.t.pension.monthlySaving}</label>
					<Input
						id="monthly"
						type="number"
						bind:value={monthlySaving}
						min="1"
						step="1"
						placeholder="20"
					/>
				</div>
				<div class="space-y-2">
					<label for="years" class="text-sm font-semibold">{i18n.t.pension.years}</label>
					<Input
						id="years"
						type="number"
						bind:value={years}
						min="1"
						max="50"
						step="1"
						placeholder="20"
					/>
				</div>
			</div>

			<div use:pressScale>
				<Button onclick={handleCalculate} disabled={isLoading} class="w-full md:w-auto">
					{isLoading ? i18n.t.common.loading : i18n.t.pension.calculate}
				</Button>
			</div>
		</CardContent>
	</Card>
</div>

{#if error}
	<div class="mt-6" use:animateIn={{ y: [10, 0], duration: 0.3 }}>
		<Card class="border-destructive">
			<CardContent class="pt-4">
				<p class="text-sm text-destructive">{error}</p>
			</CardContent>
		</Card>
	</div>
{/if}

{#if isLoading}
	<div class="mt-6 space-y-6" use:animateIn={{ opacity: [0, 1], duration: 0.2 }}>
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			{#each Array(3) as _}
				<Card>
					<CardContent class="pt-6 space-y-2">
						<Skeleton class="h-4 w-24" />
						<Skeleton class="h-8 w-32" />
					</CardContent>
				</Card>
			{/each}
		</div>
		<Card>
			<CardContent class="pt-6">
				<div class="grid grid-cols-2 gap-4">
					<Skeleton class="h-12 w-full" />
					<Skeleton class="h-12 w-full" />
				</div>
			</CardContent>
		</Card>
	</div>
{:else if !result && !error}
	<div class="mt-6 rounded-2xl border border-dashed border-border bg-muted p-8 text-center space-y-3" use:animateIn={{ y: [12, 0], delay: 0.2 }}>
		<Geo state="waiting" class="w-24 h-24 mx-auto" />
		<p class="text-muted-foreground text-sm">{i18n.t.pension.emptyState}</p>
	</div>
{/if}

{#if result}
	<div class="mt-8 space-y-6" use:animateIn={{ y: [30, 0], duration: 0.6 }}>
		<div class="flex items-center gap-3">
			<Geo state="success" class="w-16 h-16 shrink-0" />
			<div>
				<p class="text-sm font-medium text-foreground">{i18n.t.pension.resultsReady}</p>
				<Badge variant="secondary" class="text-xs font-normal mt-1">
					{i18n.t.pension.basedOnHistorical}
				</Badge>
			</div>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4" use:staggerChildren={{ y: 20, staggerDelay: 0.1 }}>
			<Card>
				<CardContent class="pt-6 space-y-2">
					<span class="text-sm text-muted-foreground">{i18n.t.pension.totalInvested}</span>
					<div class="text-2xl font-bold text-foreground tabular-nums">
						<AnimatedNumber value={result.total_invested_usd} format={formatUSD} />
					</div>
				</CardContent>
			</Card>

			<Card>
				<CardContent class="pt-6 space-y-2">
					<span class="text-sm text-muted-foreground flex items-center gap-1.5">
						<CurrencyBtc size={16} class="text-amber-500" />
						{i18n.t.pension.btcAccumulated}
					</span>
					<div class="text-2xl font-bold text-foreground tabular-nums">
						<AnimatedNumber value={result.total_btc_accumulated} format={(v) => `${v.toFixed(8)} BTC`} duration={1000} />
					</div>
				</CardContent>
			</Card>

			<Card>
				<CardContent class="pt-6 space-y-2">
					<span class="text-sm text-muted-foreground flex items-center gap-1.5">
						<TrendUp size={16} class="text-emerald-500" />
						{i18n.t.pension.currentValue}
					</span>
					<div class="text-2xl font-bold text-emerald-500 tabular-nums">
						<AnimatedNumber value={result.current_value_usd} format={formatUSD} duration={1000} />
					</div>
				</CardContent>
			</Card>
		</div>

		<div use:animateIn={{ y: [16, 0], delay: 0.3 }}>
			<Card>
				<CardContent class="pt-6">
					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-1">
							<span class="text-sm text-muted-foreground">{i18n.t.pension.avgBuyPrice}</span>
							<div class="text-lg font-semibold tabular-nums">
								<AnimatedNumber value={result.avg_buy_price} format={formatUSD} />
							</div>
						</div>
						<div class="space-y-1">
							<span class="text-sm text-muted-foreground">{i18n.t.pension.currentPrice}</span>
							<div class="text-lg font-semibold tabular-nums">
								<AnimatedNumber value={result.current_btc_price} format={formatUSD} />
							</div>
						</div>
					</div>
				</CardContent>
			</Card>
		</div>

		{#if result.monthly_data.length > 0}
			<div use:animateIn={{ y: [20, 0], delay: 0.4 }}>
				<SavingsChart data={result.monthly_data} />
			</div>
		{/if}

		<p class="text-xs text-muted-foreground text-center pt-4">{i18n.t.pension.disclaimer}</p>
	</div>
{/if}
