<script lang="ts">
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	let {
		value,
		format = (v: number) => v.toLocaleString(),
		duration = 800,
		class: className = '',
	}: {
		value: number;
		format?: (v: number) => string;
		duration?: number;
		class?: string;
	} = $props();

	const display = tweened(0, { easing: cubicOut });

	$effect(() => {
		display.set(value, { duration });
	});
</script>

<span class={className}>{format($display)}</span>
