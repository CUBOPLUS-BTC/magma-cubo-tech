<script lang="ts">
	import { api, ApiError } from '$lib/api/client';
	import { endpoints } from '$lib/api/endpoints';
	import { i18n } from '$lib/i18n/index.svelte';
	import { createQuery, createMutation, useQueryClient } from '@tanstack/svelte-query';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Badge } from '$lib/components/ui/badge';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Select from '$lib/components/ui/select';
	import Plus from 'phosphor-svelte/lib/Plus';
	import Trash from 'phosphor-svelte/lib/Trash';
	import Pause from 'phosphor-svelte/lib/Pause';
	import Play from 'phosphor-svelte/lib/Play';
	import Bell from 'phosphor-svelte/lib/Bell';
	import Calendar from 'phosphor-svelte/lib/Calendar';
	import ArrowLeft from 'phosphor-svelte/lib/ArrowLeft';
	import { animateIn, staggerChildren, pressScale } from '$lib/motion';
	import { resolve } from '$app/paths';
	import type { RecipientListResponse } from '$lib/models/recipient';
	import type {
		Reminder,
		ReminderChannel,
		ReminderCreateInput,
		ReminderListResponse,
		ReminderResponse,
	} from '$lib/models/reminder';

	const qc = useQueryClient();

	const recipientsQuery = createQuery(() => ({
		queryKey: ['recipients'],
		queryFn: () => api.get<RecipientListResponse>(endpoints.recipients.list),
	}));

	const remindersQuery = createQuery(() => ({
		queryKey: ['reminders'],
		queryFn: () => api.get<ReminderListResponse>(endpoints.reminders.list),
	}));

	let open = $state(false);
	let selectedRecipient = $state<string>('');
	let cadence = $state<'monthly' | 'biweekly'>('monthly');
	let dayOfMonth = $state(1);
	let hourLocal = $state(9);
	let channels = $state<Record<ReminderChannel, boolean>>({
		webhook: true,
		nostr_dm: false,
		email: false,
	});
	let formError = $state<string | null>(null);

	const createMutation_ = createMutation(() => ({
		mutationFn: (input: ReminderCreateInput) =>
			api.post<ReminderResponse>(endpoints.reminders.create, input),
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ['reminders'] });
			open = false;
			formError = null;
		},
		onError: (err: unknown) => {
			if (err instanceof ApiError) {
				try {
					const p = JSON.parse(err.message);
					formError = p.detail ?? err.message;
				} catch {
					formError = err.message;
				}
			} else {
				formError = String(err);
			}
		},
	}));

	const togglePauseMutation = createMutation(() => ({
		mutationFn: (r: Reminder) =>
			api.patch<ReminderResponse>(endpoints.reminders.byId(r.id), { paused: !r.paused }),
		onSuccess: () => qc.invalidateQueries({ queryKey: ['reminders'] }),
	}));

	const deleteMutation = createMutation(() => ({
		mutationFn: (id: number) =>
			api.delete<{ message: string }>(endpoints.reminders.byId(id)),
		onSuccess: () => qc.invalidateQueries({ queryKey: ['reminders'] }),
	}));

	function handleCreate() {
		formError = null;
		const rid = Number.parseInt(selectedRecipient, 10);
		if (!Number.isInteger(rid) || rid <= 0) {
			formError = 'Elegí un destinatario';
			return;
		}
		const selected = (Object.entries(channels) as [ReminderChannel, boolean][])
			.filter(([, v]) => v)
			.map(([k]) => k);
		if (selected.length === 0) {
			formError = 'Elegí al menos un canal';
			return;
		}
		createMutation_.mutate({
			recipient_id: rid,
			cadence,
			day_of_month: dayOfMonth,
			hour_local: hourLocal,
			timezone: 'America/El_Salvador',
			channels: selected,
		});
	}

	function handleDelete(r: Reminder) {
		if (!confirm('¿Eliminar este recordatorio?')) return;
		deleteMutation.mutate(r.id);
	}

	function recipientName(id: number): string {
		const list = recipientsQuery.data?.recipients ?? [];
		return list.find((r) => r.id === id)?.name ?? `#${id}`;
	}

	function formatNextFire(ts: number): string {
		const d = new Date(ts * 1000);
		return d.toLocaleString('es-SV', {
			day: 'numeric',
			month: 'short',
			hour: '2-digit',
			minute: '2-digit',
		});
	}

	function cadenceLabel(c: string): string {
		return c === 'monthly' ? 'Mensual' : c === 'biweekly' ? 'Quincenal' : 'Custom';
	}

	let recipients = $derived(recipientsQuery.data?.recipients ?? []);
	let reminders = $derived(remindersQuery.data?.reminders ?? []);
	let isLoading = $derived(remindersQuery.isLoading);
	let hasRecipients = $derived(recipients.length > 0);
</script>

<svelte:head>
	<title>Recordatorios {i18n.t.app.titleSuffix}</title>
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
			<h1 class="font-heading text-2xl font-bold tracking-tight">Recordatorios</h1>
			<p class="text-sm text-muted-foreground">
				Te avisamos cuándo enviar. Sin custodia, sin pagos automáticos: vos firmás.
			</p>
		</div>
		<div use:pressScale>
			<Button
				onclick={() => (open = true)}
				disabled={!hasRecipients}
				class="gap-2"
			>
				<Plus size={18} weight="bold" />
				Nuevo recordatorio
			</Button>
		</div>
	</div>

	{#if !hasRecipients && !recipientsQuery.isLoading}
		<div
			class="rounded-2xl border border-dashed border-border bg-muted p-8 text-center space-y-3"
			use:animateIn={{ y: [10, 0] }}
		>
			<Bell size={48} class="mx-auto text-muted-foreground" weight="regular" />
			<p class="text-sm text-muted-foreground">
				Primero agregá un destinatario para poder recordarte de él.
			</p>
			<a
				href={resolve('/remittance/recipients')}
				class="inline-block text-sm text-primary font-semibold hover:underline"
			>
				Ir a destinatarios →
			</a>
		</div>
	{:else if isLoading}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			{#each Array(3) as _}
				<Card>
					<CardContent class="pt-6 space-y-3">
						<Skeleton class="h-5 w-40" />
						<Skeleton class="h-4 w-32" />
						<Skeleton class="h-4 w-24" />
					</CardContent>
				</Card>
			{/each}
		</div>
	{:else if reminders.length === 0}
		<div
			class="rounded-2xl border border-dashed border-border bg-muted p-8 text-center space-y-3"
			use:animateIn={{ y: [10, 0] }}
		>
			<Bell size={48} class="mx-auto text-muted-foreground" weight="regular" />
			<p class="text-sm text-muted-foreground">
				No tenés recordatorios activos. Creá el primero.
			</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2" use:staggerChildren={{ y: 16, staggerDelay: 0.05 }}>
			{#each reminders as r (r.id)}
				<Card>
					<CardContent class="pt-6 space-y-4">
						<div class="flex items-start justify-between gap-3">
							<div class="min-w-0 space-y-2">
								<div class="flex items-center gap-2 flex-wrap">
									<h3 class="font-heading text-base font-semibold truncate">
										{recipientName(r.recipient_id)}
									</h3>
									<Badge variant="secondary" class="text-[10px]">{cadenceLabel(r.cadence)}</Badge>
									{#if r.paused}
										<Badge variant="outline" class="text-[10px]">En pausa</Badge>
									{/if}
								</div>
								<div class="space-y-1 text-xs text-muted-foreground">
									<p class="flex items-center gap-1.5">
										<Calendar size={12} weight="regular" />
										Próximo aviso: <span class="font-medium text-foreground">{formatNextFire(r.next_fire_at)}</span>
									</p>
									<p>Día {r.day_of_month} · {String(r.hour_local).padStart(2, '0')}:00</p>
									<p>Canales: {r.channels.join(', ')}</p>
									{#if r.fire_count > 0}
										<p>Disparado {r.fire_count} {r.fire_count === 1 ? 'vez' : 'veces'}</p>
									{/if}
								</div>
							</div>
							<div class="flex flex-col gap-1 shrink-0">
								<Button
									variant="ghost"
									size="icon"
									onclick={() => togglePauseMutation.mutate(r)}
									disabled={togglePauseMutation.isPending}
									title={r.paused ? 'Reactivar' : 'Pausar'}
								>
									{#if r.paused}
										<Play size={16} weight="fill" />
									{:else}
										<Pause size={16} weight="fill" />
									{/if}
								</Button>
								<Button
									variant="ghost"
									size="icon"
									onclick={() => handleDelete(r)}
									disabled={deleteMutation.isPending}
									class="text-muted-foreground hover:text-destructive"
									title="Eliminar"
								>
									<Trash size={16} />
								</Button>
							</div>
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
			<Dialog.Title>Nuevo recordatorio</Dialog.Title>
			<Dialog.Description>
				Te avisamos el día y la hora que elijás. Magma nunca mueve tu plata.
			</Dialog.Description>
		</Dialog.Header>
		<div class="space-y-4 py-2">
			<div class="space-y-2">
				<Label for="recipient">Destinatario</Label>
				<Select.Root type="single" bind:value={selectedRecipient}>
					<Select.Trigger id="recipient">
						{selectedRecipient
							? recipientName(Number.parseInt(selectedRecipient, 10))
							: 'Elegí un destinatario'}
					</Select.Trigger>
					<Select.Content>
						{#each recipients as r (r.id)}
							<Select.Item value={String(r.id)}>{r.name} ({r.country})</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</div>

			<div class="grid grid-cols-2 gap-3">
				<div class="space-y-2">
					<Label for="cadence">Cadencia</Label>
					<Select.Root type="single" bind:value={cadence}>
						<Select.Trigger id="cadence">{cadenceLabel(cadence)}</Select.Trigger>
						<Select.Content>
							<Select.Item value="monthly">Mensual</Select.Item>
							<Select.Item value="biweekly">Quincenal</Select.Item>
						</Select.Content>
					</Select.Root>
				</div>
				<div class="space-y-2">
					<Label for="day">Día del mes</Label>
					<Input id="day" type="number" min="1" max="28" bind:value={dayOfMonth} />
				</div>
			</div>

			<div class="space-y-2">
				<Label for="hour">Hora local (0-23)</Label>
				<Input id="hour" type="number" min="0" max="23" bind:value={hourLocal} />
				<p class="text-[11px] text-muted-foreground">Zona horaria: America/El_Salvador</p>
			</div>

			<div class="space-y-2">
				<Label>Canales de aviso</Label>
				<div class="space-y-1.5">
					<label class="flex items-center gap-2 text-sm">
						<input type="checkbox" bind:checked={channels.webhook} class="size-4" />
						Webhook (requiere suscripción previa en /webhooks)
					</label>
					<label class="flex items-center gap-2 text-sm">
						<input type="checkbox" bind:checked={channels.nostr_dm} class="size-4" />
						Nostr DM (NIP-04)
					</label>
					<label class="flex items-center gap-2 text-sm">
						<input type="checkbox" bind:checked={channels.email} class="size-4" />
						Email (requiere correo registrado)
					</label>
				</div>
			</div>

			{#if formError}
				<p class="text-xs text-destructive">{formError}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button variant="ghost" onclick={() => (open = false)}>Cancelar</Button>
			<Button onclick={handleCreate} disabled={createMutation_.isPending}>
				{createMutation_.isPending ? 'Creando...' : 'Crear'}
			</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
