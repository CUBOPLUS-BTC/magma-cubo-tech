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
