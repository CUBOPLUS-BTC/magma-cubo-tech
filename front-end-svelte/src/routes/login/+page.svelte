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

<div class="flex min-h-screen bg-muted/30">
	<div class="hidden lg:flex lg:w-1/2 lg:flex-col lg:justify-center lg:p-12 bg-primary">
		<div class="space-y-8 max-w-md mx-auto">
			<div class="flex items-center gap-3">
				<div class="flex size-12 items-center justify-center rounded-sm bg-primary-foreground">
					<Lightning class="size-7 text-primary" weight="fill" />
				</div>
				<span class="font-heading text-4xl font-bold text-primary-foreground tracking-tight">Magma</span>
			</div>
			<div class="space-y-2">
				<h1 class="font-heading text-3xl font-semibold text-primary-foreground tracking-tight">
					Bitcoin Financial Intelligence
				</h1>
				<p class="text-primary-foreground/80 text-sm leading-relaxed">
					Track your sats, analyze your wealth, and understand your financial footprint in the Bitcoin ecosystem.
				</p>
			</div>
		</div>
	</div>

	<div class="flex flex-1 items-center justify-center p-6 lg:p-12">
		<div class="w-full max-w-md space-y-8">
			<div class="lg:hidden flex items-center gap-3 justify-center mb-8">
				<div class="flex size-10 items-center justify-center rounded-sm bg-primary">
					<Lightning class="size-6 text-primary-foreground" weight="fill" />
				</div>
				<span class="font-heading text-2xl font-bold text-primary tracking-tight">Magma</span>
			</div>

			<Card class="border-border/50 bg-card shadow-sm ring-1 ring-border/50">
				<div class="p-6 space-y-6">
					<div class="space-y-1.5 text-center">
						<h2 class="font-heading text-xl font-semibold tracking-tight text-card-foreground">Connect Your Key</h2>
						<p class="text-muted-foreground text-xs">Enter your Nostr private key to get started</p>
					</div>

					<div class="space-y-4">
						<div class="space-y-2">
							<Label for="key" class="text-muted-foreground">Private Key</Label>
							<Input
								id="key"
								type="text"
								placeholder="nsec1... or hex private key"
								bind:value={key}
								class="h-10 border-input bg-background text-xs placeholder:text-muted-foreground"
							/>
						</div>

						<Button onclick={handleConnect} class="w-full h-10 bg-primary text-primary-foreground hover:bg-primary/90 font-medium">
							Connect
						</Button>
					</div>
				</div>
			</Card>

			<div class="flex items-center justify-center gap-2 text-muted-foreground">
				<Lock class="size-3.5" />
				<span class="text-xs">Your keys never leave your device</span>
			</div>

			<p class="lg:hidden text-center text-muted-foreground text-xs">
				Bitcoin Financial Intelligence
			</p>
		</div>
	</div>
</div>
