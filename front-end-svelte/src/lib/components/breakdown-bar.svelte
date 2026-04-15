<script lang="ts">
	import { cn } from '$lib/utils.js';

	let {
		label,
		score,
		maxScore
	}: {
		label: string;
		score: number;
		maxScore: number;
	} = $props();

	const percentage = $derived((score / maxScore) * 100);

	const getBarColor = (pct: number) => {
		if (pct > 80) return '#22c55e';
		if (pct > 50) return '#f97316';
		return '#eab308';
	};

	let barColor = $derived(getBarColor(percentage));
</script>

<div class="flex items-center gap-3">
	<span class="text-sm font-medium text-foreground w-36 truncate">{label}</span>
	<div class="flex-1 h-3 bg-muted rounded-none overflow-hidden">
		<div
			class="h-full rounded-none transition-all duration-500 ease-out"
			style="width: {percentage}%; background-color: {barColor};"
		></div>
	</div>
	<span class="text-sm text-muted-foreground w-24 text-right">
		{score}/{maxScore}
	</span>
</div>
