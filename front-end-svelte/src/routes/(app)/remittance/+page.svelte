<script lang="ts">
	import type { RemittanceResult } from '$lib/models/remittance';
	import { api } from '$lib/api/client';
	import { endpoints } from '$lib/api/endpoints';
	import { i18n } from '$lib/i18n/index.svelte';
	import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import * as Select from '$lib/components/ui/select';
	import ChannelCard from '$lib/components/channel-card.svelte';
	import SavingsCard from '$lib/components/savings-card.svelte';
	import Clock from 'phosphor-svelte/lib/Clock';
	import ArrowsLeftRight from 'phosphor-svelte/lib/ArrowsLeftRight';
	import Lightning from 'phosphor-svelte/lib/Lightning';
	import Geo from '$lib/components/geo.svelte';

	let amountUsd = $state(200);
	let frequency = $state<string>('monthly');
	let result = $state.raw<RemittanceResult | null>(null);
	let isLoading = $state(false);
	let error = $state<string | null>(null);

	async function handleCompare() {
		isLoading = true;
		error = null;
		result = null;

		try {
			result = await api.post<RemittanceResult>(endpoints.remittance.compare, {
				amount_usd: amountUsd,
				frequency: frequency as 'monthly' | 'biweekly' | 'weekly'
			});
		} catch (e) {
			error = e instanceof Error ? e.message : i18n.t.remittance.errorFetch;
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>{i18n.t.remittance.title} {i18n.t.app.titleSuffix}</title>
	<meta name="description" content={i18n.t.remittance.subtitle} />
</svelte:head>

<div class="space-y-8">
	<div>
		<h1 class="font-heading text-2xl font-bold tracking-tight">{i18n.t.remittance.title}</h1>
		<p class="text-sm text-muted-foreground mt-1">{i18n.t.remittance.corridor}</p>
	</div>

	<div class="flex items-start gap-2 rounded-xl border border-primary/20 bg-primary/5 p-4">
		<Lightning size={18} class="text-primary mt-0.5 shrink-0" />
		<p class="text-sm text-primary/80">{i18n.t.remittance.legalTender}</p>
	</div>

	<Card>
		<CardHeader>
			<CardTitle class="font-heading">{i18n.t.remittance.compareOptions}</CardTitle>
		</CardHeader>
		<CardContent class="space-y-6">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div class="space-y-2">
					<label for="amount" class="text-sm font-semibold">{i18n.t.remittance.amount}</label>
					<Input
						id="amount"
						type="number"
						bind:value={amountUsd}
						min="1"
						step="1"
						placeholder="Enter amount"
					/>
				</div>

				<div class="space-y-2">
					<label for="frequency" class="text-sm font-semibold">{i18n.t.remittance.frequency}</label>
					<Select.Root type="single" bind:value={frequency}>
						<Select.Trigger id="frequency">
							{i18n.t.remittance.frequencies[frequency as keyof typeof i18n.t.remittance.frequencies] ?? frequency}
						</Select.Trigger>
						<Select.Content>
							<Select.Item value="monthly">{i18n.t.remittance.frequencies.monthly}</Select.Item>
							<Select.Item value="biweekly">{i18n.t.remittance.frequencies.biweekly}</Select.Item>
							<Select.Item value="weekly">{i18n.t.remittance.frequencies.weekly}</Select.Item>
						</Select.Content>
					</Select.Root>
				</div>
			</div>

			<Button onclick={handleCompare} disabled={isLoading} class="w-full md:w-auto">
				{isLoading ? i18n.t.remittance.comparing : i18n.t.remittance.compare}
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
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<Card>
					<CardContent class="pt-6 space-y-4">
						<Skeleton class="h-4 w-32" />
						<Skeleton class="h-8 w-24" />
						<Skeleton class="h-4 w-full" />
					</CardContent>
				</Card>
				<Card>
					<CardContent class="pt-6 space-y-4">
						<Skeleton class="h-4 w-32" />
						<Skeleton class="h-8 w-24" />
						<Skeleton class="h-4 w-full" />
					</CardContent>
				</Card>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Card>
					<CardContent class="pt-6 space-y-3">
						<Skeleton class="h-5 w-20" />
						<Skeleton class="h-6 w-16" />
						<Skeleton class="h-4 w-full" />
					</CardContent>
				</Card>
				<Card>
					<CardContent class="pt-6 space-y-3">
						<Skeleton class="h-5 w-20" />
						<Skeleton class="h-6 w-16" />
						<Skeleton class="h-4 w-full" />
					</CardContent>
				</Card>
				<Card>
					<CardContent class="pt-6 space-y-3">
						<Skeleton class="h-5 w-20" />
						<Skeleton class="h-6 w-16" />
						<Skeleton class="h-4 w-full" />
					</CardContent>
				</Card>
			</div>
		</div>
	{:else if !result}
		<div class="rounded-2xl border border-dashed border-border bg-muted/30 p-8 text-center space-y-3">
			<Geo state="waiting" class="w-24 h-24 mx-auto" />
			<p class="text-muted-foreground text-sm">{i18n.t.remittance.subtitle}</p>
		</div>
	{/if}

	{#if result}
		<div class="space-y-6">
			<div class="flex items-center gap-3">
				<Geo state="success" class="w-16 h-16 shrink-0" />
				<p class="text-sm font-medium text-foreground">{i18n.t.remittance.resultsReady}</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<SavingsCard annualSavings={result.annual_savings} bestChannel={result.best_channel} />

				{#if result.best_time}
					<Card>
						<CardHeader>
							<CardTitle class="flex items-center gap-2 text-sm font-medium text-muted-foreground">
								<Clock size={18} weight="regular" />
								{i18n.t.remittance.bestTime}
							</CardTitle>
						</CardHeader>
						<CardContent class="space-y-3">
							<div class="text-2xl font-bold text-foreground">
								{result.best_time.best_time}
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-muted-foreground">{i18n.t.remittance.currentFee}</span>
								<span class="text-sm font-medium tabular-nums">{result.best_time.current_fee_sat_vb} sat/vB</span>
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-muted-foreground">{i18n.t.remittance.lowFee}</span>
								<span class="text-sm font-medium tabular-nums text-green-600 dark:text-green-500">{result.best_time.estimated_low_fee_sat_vb} sat/vB</span>
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-muted-foreground">{i18n.t.remittance.savings}</span>
								<Badge variant="secondary">
									{result.best_time.savings_percent}%
								</Badge>
							</div>
						</CardContent>
					</Card>
				{/if}
			</div>

			<div>
				<h2 class="font-heading text-lg font-semibold mb-4">{i18n.t.remittance.availableChannels}</h2>
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					{#each result.channels as channel (channel.name)}
						<ChannelCard {channel} />
					{/each}
				</div>
			</div>
		</div>
	{/if}
</div>
