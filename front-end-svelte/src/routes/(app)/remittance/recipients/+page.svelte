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
	import Lightning from 'phosphor-svelte/lib/Lightning';
	import UserCircle from 'phosphor-svelte/lib/UserCircle';
	import ArrowLeft from 'phosphor-svelte/lib/ArrowLeft';
	import type {
		Recipient,
		RecipientCreateInput,
		RecipientListResponse,
		RecipientResponse,
	} from '$lib/models/recipient';
	import { animateIn, staggerChildren, pressScale } from '$lib/motion';
	import { resolve } from '$app/paths';
	import Wallet from 'phosphor-svelte/lib/Wallet';

	const qc = useQueryClient();

	const listQuery = createQuery(() => ({
		queryKey: ['recipients'],
		queryFn: () => api.get<RecipientListResponse>(endpoints.recipients.list),
	}));

	let open = $state(false);
	let name = $state('');
	let lightningAddress = $state('');
	let country = $state('SV');
	let defaultAmount = $state<number | null>(200);
	let formError = $state<string | null>(null);

	const countries = ['SV', 'MX', 'GT', 'HN', 'NI', 'CR', 'US', 'ES'] as const;

	const createMutation_ = createMutation(() => ({
		mutationFn: (input: RecipientCreateInput) =>
			api.post<RecipientResponse>(endpoints.recipients.create, input),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ['recipients'] });
			open = false;
			name = '';
			lightningAddress = '';
			country = 'SV';
			defaultAmount = 200;
			formError = null;
		},
		onError: (err: unknown) => {
			if (err instanceof ApiError) {
				try {
					const payload = JSON.parse(err.message);
					formError = payload.detail ?? err.message;
				} catch {
					formError = err.message;
				}
			} else {
				formError = String(err);
			}
		},
	}));

	const deleteMutation = createMutation(() => ({
		mutationFn: (id: number) =>
			api.delete<{ message: string; id: number }>(endpoints.recipients.byId(id)),
		onSuccess: () => qc.invalidateQueries({ queryKey: ['recipients'] }),
	}));

	function handleCreate() {
		formError = null;
		if (!name.trim()) {
			formError = 'Ingresá un nombre';
			return;
		}
		if (!lightningAddress.includes('@')) {
			formError = 'Lightning address inválida';
			return;
		}
		createMutation_.mutate({
			name: name.trim(),
			lightning_address: lightningAddress.trim().toLowerCase(),
			country,
			default_amount_usd: defaultAmount,
		});
	}

	function handleDelete(r: Recipient) {
		if (!confirm(`¿Eliminar a ${r.name}?`)) return;
		deleteMutation.mutate(r.id);
	}

	let recipients = $derived(listQuery.data?.recipients ?? []);
	let isLoading = $derived(listQuery.isLoading);
</script>

<svelte:head>
	<title>Destinatarios {i18n.t.app.titleSuffix}</title>
</svelte:head>

<div class="space-y-8">
	<div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
		<div class="space-y-1">
			<a
				href={resolve('/remittance')}
				class="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
			>
				<ArrowLeft size={14} weight="bold" />
				Volver a remesas
			</a>
			<h1 class="font-heading text-2xl font-bold tracking-tight">Destinatarios</h1>
			<p class="text-sm text-muted-foreground">Guardá a tus familiares y enviá con un click.</p>
		</div>
		<div use:pressScale>
			<Button onclick={() => (open = true)} class="gap-2">
				<Plus size={18} weight="bold" />
				Nuevo destinatario
			</Button>
		</div>
	</div>

	{#if isLoading}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			{#each Array(4) as _}
				<Card>
					<CardContent class="pt-6 space-y-3">
						<Skeleton class="h-5 w-32" />
						<Skeleton class="h-4 w-48" />
						<Skeleton class="h-4 w-24" />
					</CardContent>
				</Card>
			{/each}
		</div>
	{:else if recipients.length === 0}
		<div
			class="rounded-2xl border border-dashed border-border bg-muted p-8 text-center space-y-3"
			use:animateIn={{ y: [10, 0] }}
		>
			<UserCircle size={48} class="mx-auto text-muted-foreground" weight="regular" />
			<p class="text-sm text-muted-foreground">
				Aún no tenés destinatarios. Agregá al primero para empezar.
			</p>
			<a
				href={resolve('/wallets')}
				class="inline-flex items-center gap-1.5 text-xs text-primary hover:underline mt-1"
			>
				<Wallet size={12} />
				{i18n.t.wallets.tipRecipients}
			</a>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2" use:staggerChildren={{ y: 16, staggerDelay: 0.05 }}>
			{#each recipients as r (r.id)}
				<Card>
					<CardContent class="pt-6 space-y-3">
						<div class="flex items-start justify-between gap-3">
							<div class="min-w-0 space-y-1">
								<div class="flex items-center gap-2">
									<h3 class="font-heading text-base font-semibold truncate">{r.name}</h3>
									<Badge variant="secondary" class="text-[10px]">{r.country}</Badge>
								</div>
								<p class="text-xs text-muted-foreground truncate flex items-center gap-1.5">
									<Lightning size={12} weight="fill" class="text-amber-500 shrink-0" />
									{r.lightning_address}
								</p>
								{#if r.default_amount_usd}
									<p class="text-sm text-foreground font-medium">
										${r.default_amount_usd.toFixed(0)} USD
										<span class="text-muted-foreground font-normal">por envío</span>
									</p>
								{/if}
							</div>
							<Button
								variant="ghost"
								size="icon"
								onclick={() => handleDelete(r)}
								disabled={deleteMutation.isPending}
								class="text-muted-foreground hover:text-destructive shrink-0"
							>
								<Trash size={16} />
							</Button>
						</div>
					</CardContent>
				</Card>
			{/each}
		</div>
	{/if}
</div>

<Dialog.Root bind:open>
	<Dialog.Content class="sm:max-w-md">
		<Dialog.Header>
			<Dialog.Title>Nuevo destinatario</Dialog.Title>
			<Dialog.Description>
				Validamos la Lightning address contra la wallet receptora antes de guardarla.
				<a href={resolve('/wallets')} class="text-primary hover:underline ml-1">{i18n.t.wallets.seeGuide} &rarr;</a>
			</Dialog.Description>
		</Dialog.Header>
		<div class="space-y-4 py-2">
			<div class="space-y-2">
				<Label for="name">Nombre</Label>
				<Input id="name" bind:value={name} placeholder="Mamá" maxlength={80} />
			</div>
			<div class="space-y-2">
				<Label for="ln-address">Lightning address</Label>
				<Input
					id="ln-address"
					bind:value={lightningAddress}
					placeholder="maria@blink.sv"
					autocomplete="off"
					autocapitalize="none"
				/>
			</div>
			<div class="grid grid-cols-2 gap-3">
				<div class="space-y-2">
					<Label for="country">País</Label>
					<Select.Root type="single" bind:value={country}>
						<Select.Trigger id="country">{country}</Select.Trigger>
						<Select.Content>
							{#each countries as c}
								<Select.Item value={c}>{c}</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				</div>
				<div class="space-y-2">
					<Label for="amount">Monto default (USD)</Label>
					<Input
						id="amount"
						type="number"
						bind:value={defaultAmount}
						min="1"
						step="1"
						placeholder="200"
					/>
				</div>
			</div>
			{#if formError}
				<p class="text-xs text-destructive">{formError}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button variant="ghost" onclick={() => (open = false)}>Cancelar</Button>
			<Button onclick={handleCreate} disabled={createMutation_.isPending}>
				{createMutation_.isPending ? 'Validando LNURL...' : 'Crear'}
			</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
