<script lang="ts">
	import { api, ApiError } from '$lib/api/client';
	import { endpoints } from '$lib/api/endpoints';
	import { i18n } from '$lib/i18n/index.svelte';
	import { createQuery, createMutation, useQueryClient } from '@tanstack/svelte-query';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Badge } from '$lib/components/ui/badge';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Select from '$lib/components/ui/select';
	import Plus from 'phosphor-svelte/lib/Plus';
	import Trash from 'phosphor-svelte/lib/Trash';
	import GitFork from 'phosphor-svelte/lib/GitFork';
	import ArrowLeft from 'phosphor-svelte/lib/ArrowLeft';
	import Lightning from 'phosphor-svelte/lib/Lightning';
	import ShieldCheck from 'phosphor-svelte/lib/ShieldCheck';
	import Copy from 'phosphor-svelte/lib/Copy';
	import Check from 'phosphor-svelte/lib/Check';
	import { animateIn, staggerChildren } from '$lib/motion';
	import { resolve } from '$app/paths';
	import { springHover, pressScale as pressScaleAction } from '$lib/motion';

	const qc = useQueryClient();

	// ---- Types ----
	interface SplitRule {
		id?: number;
		recipient_id: number;
		percentage: number;
		priority: number;
		label: string;
		recipient_name?: string;
		recipient_ln?: string;
	}
	interface SplitProfile {
		id: number;
		label: string;
		is_active: number;
		rules: SplitRule[];
		created_at: number;
	}
	interface Recipient {
		id: number;
		name: string;
		lightning_address: string;
	}
	interface SplitInvoice {
		rule: { recipient_name: string; recipient_ln: string; percentage: number; label: string };
		amount_usd: number;
		amount_sats: number;
		bolt11: string | null;
		deeplink: string | null;
		status: 'ready' | 'error' | 'skip';
		error?: string;
	}
	interface BuildResult {
		profile: { id: number; label: string };
		total_usd: number;
		total_sats: number;
		btc_price_usd: number;
		invoices: SplitInvoice[];
		all_ready: boolean;
		custody_model: string;
	}

	// ---- Queries ----
	const profilesQuery = createQuery(() => ({
		queryKey: ['split-profiles'],
		queryFn: () => api.get<{ profiles: SplitProfile[] }>(endpoints.splits.list),
	}));
	const recipientsQuery = createQuery(() => ({
		queryKey: ['recipients'],
		queryFn: () => api.get<{ recipients: Recipient[] }>(endpoints.recipients.list),
	}));

	let profiles = $derived(profilesQuery.data?.profiles ?? []);
	let recipients = $derived(recipientsQuery.data?.recipients ?? []);

	// ---- Create profile ----
	let createOpen = $state(false);
	let newLabel = $state('');
	let createError = $state<string | null>(null);

	const createMut = createMutation(() => ({
		mutationFn: (label: string) => api.post<SplitProfile>(endpoints.splits.create, { label }),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ['split-profiles'] });
			createOpen = false;
			newLabel = '';
			createError = null;
		},
		onError: (e: Error) => { createError = e.message; },
	}));

	function handleCreate() {
		if (!newLabel.trim()) return;
		createError = null;
		createMut.mutate(newLabel.trim());
	}

	// ---- Delete profile ----
	const deleteMut = createMutation(() => ({
		mutationFn: (id: number) => api.delete(endpoints.splits.byId(id)),
		onSuccess: () => { qc.invalidateQueries({ queryKey: ['split-profiles'] }); },
	}));

	// ---- Edit rules ----
	let editingProfile = $state<SplitProfile | null>(null);
	let editRules = $state<SplitRule[]>([]);
	let rulesError = $state<string | null>(null);

	function startEditRules(p: SplitProfile) {
		editingProfile = p;
		editRules = p.rules.length
			? p.rules.map(r => ({ ...r }))
			: [{ recipient_id: recipients[0]?.id ?? 0, percentage: 100, priority: 0, label: '' }];
		rulesError = null;
	}

	function addRule() {
		editRules = [...editRules, { recipient_id: recipients[0]?.id ?? 0, percentage: 0, priority: editRules.length, label: '' }];
	}

	function removeRule(idx: number) {
		editRules = editRules.filter((_, i) => i !== idx);
	}

	let rulesTotal = $derived(editRules.reduce((s, r) => s + (r.percentage || 0), 0));

	const rulesMut = createMutation(() => ({
		mutationFn: ({ id, rules }: { id: number; rules: SplitRule[] }) =>
			api.put<{ rules: SplitRule[] }>(endpoints.splits.rules(id), { rules }),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ['split-profiles'] });
			editingProfile = null;
			rulesError = null;
		},
		onError: (e: Error) => { rulesError = e.message; },
	}));

	function handleSaveRules() {
		if (!editingProfile) return;
		if (rulesTotal !== 100) { rulesError = i18n.t.splits.totalMustBe100; return; }
		rulesError = null;
		rulesMut.mutate({
			id: editingProfile.id,
			rules: editRules.map((r, i) => ({
				recipient_id: r.recipient_id,
				percentage: r.percentage,
				priority: i,
				label: r.label,
			})),
		});
	}

	// ---- Build split ----
	let buildProfile = $state<SplitProfile | null>(null);
	let buildAmount = $state(200);
	let buildComment = $state('');
	let buildResult = $state<BuildResult | null>(null);
	let buildError = $state<string | null>(null);

	const buildMut = createMutation(() => ({
		mutationFn: (input: { profile_id: number; amount_usd: number; comment?: string }) =>
			api.post<BuildResult>(endpoints.splits.build, input),
		onSuccess: (data: BuildResult) => { buildResult = data; buildError = null; },
		onError: (e: Error) => { buildError = e.message; buildResult = null; },
	}));

	function handleBuild() {
		if (!buildProfile) return;
		buildError = null;
		buildResult = null;
		buildMut.mutate({
			profile_id: buildProfile.id,
			amount_usd: buildAmount,
			comment: buildComment || undefined,
		});
	}

	// ---- Copy invoice ----
	let copiedIdx = $state<number | null>(null);
	async function copyInvoice(bolt11: string, idx: number) {
		await navigator.clipboard.writeText(bolt11);
		copiedIdx = idx;
		setTimeout(() => { copiedIdx = null; }, 2000);
	}
</script>

<svelte:head>
	<title>{i18n.t.splits.title} {i18n.t.app.titleSuffix}</title>
</svelte:head>

<div class="space-y-8" use:staggerChildren={{ y: 20, staggerDelay: 0.08 }}>
	<!-- Header -->
	<div class="flex items-start justify-between">
		<div>
			<a href={resolve('/remittance')} class="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground mb-3 transition-colors">
				<ArrowLeft size={14} weight="bold" /> Remesas
			</a>
			<h1 class="font-heading text-2xl font-bold tracking-tight flex items-center gap-2">
				<GitFork size={28} class="text-emerald-500" weight="bold" />
				{i18n.t.splits.title}
			</h1>
			<p class="text-sm text-muted-foreground mt-1">{i18n.t.splits.subtitle}</p>
		</div>
		<Button size="sm" onclick={() => { createOpen = true; }}>
			<Plus size={16} class="mr-1" /> {i18n.t.splits.newProfile}
		</Button>
	</div>

	<!-- Non-custodial badge -->
	<div class="flex items-center gap-2 rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-4 py-3">
		<ShieldCheck size={20} class="text-emerald-500 shrink-0" weight="fill" />
		<div>
			<span class="text-sm font-semibold text-emerald-600 dark:text-emerald-400">{i18n.t.splits.custodyBadge}</span>
			<p class="text-xs text-muted-foreground">{i18n.t.splits.custodyExplain}</p>
		</div>
	</div>

	<!-- No recipients warning -->
	{#if recipientsQuery.isSuccess && recipients.length === 0}
		<Card class="border-dashed">
			<CardContent class="pt-6 text-center text-sm text-muted-foreground">
				{i18n.t.splits.noRecipients}
				<a href={resolve('/remittance/recipients')} class="text-primary underline ml-1">Ir a destinatarios</a>
			</CardContent>
		</Card>
	{/if}

	<!-- Loading -->
	{#if profilesQuery.isLoading}
		<div class="space-y-4">
			{#each [1, 2] as _}<Skeleton class="h-28 w-full rounded-xl" />{/each}
		</div>
	{/if}

	<!-- Profiles list -->
	{#if profilesQuery.isSuccess && profiles.length === 0 && recipients.length > 0}
		<Card class="border-dashed">
			<CardContent class="pt-6 text-center text-sm text-muted-foreground">
				{i18n.t.splits.noProfiles}
			</CardContent>
		</Card>
	{/if}

	{#each profiles as profile (profile.id)}
		<Card>
			<CardHeader class="pb-3">
				<div class="flex items-center justify-between">
					<CardTitle class="font-heading text-base">{profile.label}</CardTitle>
					<div class="flex items-center gap-2">
						<Badge variant="outline" class="text-emerald-600">{i18n.t.splits.active}</Badge>
						<Button variant="ghost" size="sm" class="text-red-500 h-8 w-8 p-0"
							onclick={() => { if (confirm(i18n.t.splits.deleteConfirm)) deleteMut.mutate(profile.id); }}>
							<Trash size={16} />
						</Button>
					</div>
				</div>
			</CardHeader>
			<CardContent class="space-y-4">
				<!-- Rules display -->
				{#if profile.rules.length === 0}
					<p class="text-sm text-muted-foreground">Sin reglas configuradas.</p>
				{:else}
					<div class="space-y-2">
						{#each profile.rules as rule}
							<div class="flex items-center gap-3 rounded-lg bg-muted/50 px-3 py-2 text-sm">
								<span class="font-mono font-semibold text-primary w-12 text-right">{rule.percentage}%</span>
								<Lightning size={14} class="text-amber-500" />
								<span class="truncate">{rule.recipient_name ?? ''}</span>
								<span class="text-xs text-muted-foreground truncate">{rule.recipient_ln ?? ''}</span>
								{#if rule.label}
									<Badge variant="secondary" class="ml-auto text-xs">{rule.label}</Badge>
								{/if}
							</div>
						{/each}
					</div>
				{/if}

				<!-- Actions -->
				<div class="flex gap-2 pt-2">
					<Button variant="outline" size="sm" onclick={() => startEditRules(profile)}
						disabled={recipients.length === 0}>
						{i18n.t.splits.rules}
					</Button>
					<Button size="sm" onclick={() => { buildProfile = profile; buildResult = null; buildError = null; }}
						disabled={profile.rules.length === 0}>
						<Lightning size={14} class="mr-1" /> {i18n.t.splits.buildSplit}
					</Button>
				</div>
			</CardContent>
		</Card>
	{/each}
</div>

<!-- Create profile dialog -->
<Dialog.Root bind:open={createOpen}>
	<Dialog.Content class="sm:max-w-md">
		<Dialog.Header>
			<Dialog.Title>{i18n.t.splits.newProfile}</Dialog.Title>
		</Dialog.Header>
		<div class="space-y-4 py-4">
			<div class="space-y-2">
				<Label>{i18n.t.splits.profileLabel}</Label>
				<Input bind:value={newLabel} placeholder={i18n.t.splits.profileLabelPlaceholder} />
			</div>
			{#if createError}
				<p class="text-sm text-red-500">{createError}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button onclick={handleCreate} disabled={createMut.isPending || !newLabel.trim()}>
				{createMut.isPending ? i18n.t.splits.saving : i18n.t.splits.newProfile}
			</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<!-- Edit rules dialog -->
<Dialog.Root open={editingProfile !== null} onOpenChange={(v) => { if (!v) editingProfile = null; }}>
	<Dialog.Content class="sm:max-w-lg">
		<Dialog.Header>
			<Dialog.Title>{i18n.t.splits.rules}: {editingProfile?.label ?? ''}</Dialog.Title>
		</Dialog.Header>
		<div class="space-y-4 py-4 max-h-[60vh] overflow-y-auto">
			{#each editRules as rule, idx}
				<div class="flex items-end gap-2 rounded-lg border p-3">
					<div class="flex-1 space-y-2">
						<Label>{i18n.t.splits.recipient}</Label>
						<Select.Root type="single" value={String(rule.recipient_id)} onValueChange={(v) => { editRules[idx].recipient_id = Number(v); }}>
							<Select.Trigger class="w-full">
								{recipients.find(r => r.id === rule.recipient_id)?.name ?? 'Seleccionar'}
							</Select.Trigger>
							<Select.Content>
								{#each recipients as r}
									<Select.Item value={String(r.id)}>{r.name} ({r.lightning_address})</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
					</div>
					<div class="w-20 space-y-2">
						<Label>{i18n.t.splits.percentage}</Label>
						<Input type="number" min="1" max="100" bind:value={editRules[idx].percentage} />
					</div>
					<div class="flex-1 space-y-2">
						<Label>{i18n.t.splits.label}</Label>
						<Input bind:value={editRules[idx].label} placeholder={i18n.t.splits.labelPlaceholder} />
					</div>
					<Button variant="ghost" size="sm" class="text-red-500 shrink-0 h-9 w-9 p-0"
						onclick={() => removeRule(idx)} disabled={editRules.length <= 1}>
						<Trash size={16} />
					</Button>
				</div>
			{/each}

			<Button variant="outline" size="sm" onclick={addRule} class="w-full">
				<Plus size={14} class="mr-1" /> {i18n.t.splits.addRule}
			</Button>

			<!-- Total indicator -->
			<div class="flex items-center justify-between text-sm font-semibold px-1">
				<span>Total</span>
				<span class={rulesTotal === 100 ? 'text-emerald-500' : 'text-red-500'}>
					{rulesTotal}%
				</span>
			</div>

			{#if rulesError}
				<p class="text-sm text-red-500">{rulesError}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button onclick={handleSaveRules} disabled={rulesMut.isPending || rulesTotal !== 100}>
				{rulesMut.isPending ? i18n.t.splits.saving : i18n.t.splits.saveRules}
			</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<!-- Build split dialog -->
<Dialog.Root open={buildProfile !== null} onOpenChange={(v) => { if (!v) { buildProfile = null; buildResult = null; } }}>
	<Dialog.Content class="sm:max-w-xl">
		<Dialog.Header>
			<Dialog.Title class="flex items-center gap-2">
				<Lightning size={20} class="text-amber-500" />
				{i18n.t.splits.buildSplit}: {buildProfile?.label ?? ''}
			</Dialog.Title>
		</Dialog.Header>

		{#if !buildResult}
			<!-- Input form -->
			<div class="space-y-4 py-4">
				<div class="space-y-2">
					<Label>{i18n.t.splits.amountUsd}</Label>
					<Input type="number" min="1" bind:value={buildAmount} />
				</div>
				<div class="space-y-2">
					<Label>{i18n.t.splits.comment}</Label>
					<Input bind:value={buildComment} placeholder="Remesa mensual..." />
				</div>
				{#if buildError}
					<p class="text-sm text-red-500">{buildError}</p>
				{/if}
			</div>
			<Dialog.Footer>
				<Button onclick={handleBuild} disabled={buildMut.isPending || buildAmount <= 0}>
					{#if buildMut.isPending}
						<span class="animate-pulse">{i18n.t.splits.building}</span>
					{:else}
						<Lightning size={14} class="mr-1" /> {i18n.t.splits.buildSplit}
					{/if}
				</Button>
			</Dialog.Footer>
		{:else}
			<!-- Results -->
			<div class="space-y-4 py-4 max-h-[65vh] overflow-y-auto">
				<div class="flex items-center justify-between text-sm">
					<span class="text-muted-foreground">Total</span>
					<span class="font-semibold">${buildResult.total_usd} = {buildResult.total_sats.toLocaleString()} sats</span>
				</div>
				<div class="flex items-center justify-between text-sm">
					<span class="text-muted-foreground">BTC Price</span>
					<span class="font-mono">${buildResult.btc_price_usd.toLocaleString()}</span>
				</div>

				<Badge variant={buildResult.all_ready ? 'default' : 'destructive'} class="w-full justify-center py-1.5">
					{buildResult.all_ready ? i18n.t.splits.invoicesReady : i18n.t.splits.invoicesPartial}
				</Badge>

				<p class="text-xs text-muted-foreground text-center">{i18n.t.splits.payEach}</p>

				{#each buildResult.invoices as inv, idx}
					<div class="rounded-lg border p-4 space-y-3 {inv.status === 'ready' ? 'border-emerald-500/30' : 'border-red-500/30'}">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								<span class="font-mono font-semibold text-primary">{inv.rule.percentage}%</span>
								<span class="text-sm font-semibold">{inv.rule.recipient_name}</span>
								{#if inv.rule.label}
									<Badge variant="secondary" class="text-xs">{inv.rule.label}</Badge>
								{/if}
							</div>
							<Badge variant={inv.status === 'ready' ? 'outline' : 'destructive'} class="text-xs">
								{i18n.t.splits.status[inv.status]}
							</Badge>
						</div>

						<div class="text-sm text-muted-foreground">
							${inv.amount_usd} = {inv.amount_sats.toLocaleString()} sats
						</div>

						{#if inv.bolt11}
							<div class="flex gap-2">
								<code class="flex-1 text-xs bg-muted rounded px-2 py-1.5 truncate font-mono">
									{inv.bolt11.slice(0, 40)}...
								</code>
								<Button variant="outline" size="sm" class="shrink-0"
									onclick={() => copyInvoice(inv.bolt11!, idx)}>
									{#if copiedIdx === idx}
										<Check size={14} class="text-emerald-500" />
									{:else}
										<Copy size={14} />
									{/if}
								</Button>
								<Button size="sm" class="shrink-0"
									onclick={() => window.open(inv.deeplink!, '_self')}>
									<Lightning size={14} class="mr-1" /> {i18n.t.splits.openWallet}
								</Button>
							</div>
						{:else if inv.error}
							<p class="text-xs text-red-500">{inv.error}</p>
						{/if}
					</div>
				{/each}
			</div>
		{/if}
	</Dialog.Content>
</Dialog.Root>
