<script lang="ts">
	import type { PensionProjection } from '$lib/models/pension';
	import { api } from '$lib/api/client';
	import { endpoints } from '$lib/api/endpoints';
	import { i18n } from '$lib/i18n/index.svelte';
	import { formatUSD } from '$lib/utils/formatters';
	import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import PiggyBank from 'phosphor-svelte/lib/PiggyBank';
	import CurrencyBtc from 'phosphor-svelte/lib/CurrencyBtc';
	import TrendUp from 'phosphor-svelte/lib/TrendUp';
	import Warning from 'phosphor-svelte/lib/Warning';
	import Geo from '$lib/components/geo.svelte';
	import SavingsChart from '$lib/components/savings-chart.svelte';

	let monthlySaving = $state(20);
	let years = $state(20);
	let result = $state.raw<PensionProjection | null>(null);
	let isLoading = $state(false);
	let error = $state<string | null>(null);

	async function handleCalculate() {
		isLoading = true;
		error = null;
		result = null;

		try {
			result = await api.post<PensionProjection>(endpoints.pension.projection, {
				monthly_saving_usd: monthlySaving,
				years,
			});
		} catch (e) {
			error = e instanceof Error ? e.message : i18n.t.pension.errorFetch;
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>{i18n.t.pension.title} {i18n.t.app.titleSuffix}</title>
</svelte:head>

<div class="space-y-8">
	<div>
		<h1 class="font-heading text-2xl font-bold tracking-tight">{i18n.t.pension.title}</h1>
		<p class="text-sm text-muted-foreground mt-1">{i18n.t.pension.subtitle}</p>
	</div>

	<Card>
		<CardHeader>
			<CardTitle class="font-heading flex items-center gap-2">
				<PiggyBank size={20} class="text-primary" />
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

			<Button onclick={handleCalculate} disabled={isLoading} class="w-full md:w-auto">
				{isLoading ? i18n.t.common.loading : i18n.t.pension.calculate}
			</Button>
		</CardContent>
	</Card>

	{#if error}
		<Card class="border-destructive">
			<CardContent class="pt-4">
				<p class="text-sm text-destructive">{error}</p>
			</CardContent>
		</Card>
	{/if}

	{#if isLoading}
		<div class="space-y-6">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Card>
					<CardContent class="pt-6 space-y-2">
						<Skeleton class="h-4 w-24" />
						<Skeleton class="h-8 w-32" />
					</CardContent>
				</Card>
				<Card>
					<CardContent class="pt-6 space-y-2">
						<Skeleton class="h-4 w-24" />
						<Skeleton class="h-8 w-32" />
					</CardContent>
				</Card>
				<Card>
					<CardContent class="pt-6 space-y-2">
						<Skeleton class="h-4 w-24" />
						<Skeleton class="h-8 w-32" />
					</CardContent>
				</Card>
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
	{:else if !result}
		<div class="rounded-2xl border border-dashed border-border bg-muted/30 p-8 text-center space-y-3">
			<Geo state="waiting" class="w-24 h-24 mx-auto" />
			<p class="text-muted-foreground text-sm">{i18n.t.pension.emptyState}</p>
		</div>
	{/if}

	{#if result}
		<div class="space-y-6">
			<div class="flex items-center gap-3">
				<Geo state="success" class="w-16 h-16 shrink-0" />
				<div>
					<p class="text-sm font-medium text-foreground">{i18n.t.pension.resultsReady}</p>
					<Badge variant="secondary" class="text-xs font-normal mt-1">
						{i18n.t.pension.basedOnHistorical}
					</Badge>
				</div>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Card>
					<CardContent class="pt-6 space-y-2">
						<span class="text-sm text-muted-foreground">{i18n.t.pension.totalInvested}</span>
						<div class="text-2xl font-bold text-foreground tabular-nums">
							{formatUSD(result.total_invested_usd)}
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent class="pt-6 space-y-2">
						<span class="text-sm text-muted-foreground flex items-center gap-1.5">
							<CurrencyBtc size={16} />
							{i18n.t.pension.btcAccumulated}
						</span>
						<div class="text-2xl font-bold text-foreground tabular-nums">
							{result.total_btc_accumulated.toFixed(8)} BTC
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent class="pt-6 space-y-2">
						<span class="text-sm text-muted-foreground flex items-center gap-1.5">
							<TrendUp size={16} />
							{i18n.t.pension.currentValue}
						</span>
						<div class="text-2xl font-bold text-primary tabular-nums">
							{formatUSD(result.current_value_usd)}
						</div>
					</CardContent>
				</Card>
			</div>

			<Card>
				<CardContent class="pt-6">
					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-1">
							<span class="text-sm text-muted-foreground">{i18n.t.pension.avgBuyPrice}</span>
							<div class="text-lg font-semibold tabular-nums">{formatUSD(result.avg_buy_price)}</div>
						</div>
						<div class="space-y-1">
							<span class="text-sm text-muted-foreground">{i18n.t.pension.currentPrice}</span>
							<div class="text-lg font-semibold tabular-nums">{formatUSD(result.current_btc_price)}</div>
						</div>
					</div>
				</CardContent>
			</Card>

			{#if result.monthly_data.length > 0}
				<SavingsChart data={result.monthly_data} />
			{/if}

			<div class="flex items-start gap-2 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
				<Warning size={18} class="text-amber-600 dark:text-amber-400 mt-0.5 shrink-0" />
				<p class="text-sm text-amber-700 dark:text-amber-300">{i18n.t.pension.disclaimer}</p>
			</div>
		</div>
	{/if}
</div>
