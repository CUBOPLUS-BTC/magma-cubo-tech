<script lang="ts">
	import { cn } from '$lib/utils.js';
	import { Badge } from '$lib/components/ui/badge';

	let { score, rank }: { score: number; rank: string } = $props();

	const radius = 80;
	const strokeWidth = 12;
	const normalizedRadius = radius - strokeWidth / 2;
	const circumference = normalizedRadius * Math.PI;
	const maxScore = 750;

	const getArcColor = (s: number) => {
		if (s > 600) return '#22c55e';
		if (s > 400) return '#f97316';
		if (s > 200) return '#eab308';
		return '#ef4444';
	};

	let strokeDashoffset = $derived(circumference - (score / maxScore) * circumference);
	let arcColor = $derived(getArcColor(score));
</script>

<div class="flex flex-col items-center gap-2">
	<svg
		width={radius * 2 + strokeWidth}
		height={(radius + strokeWidth / 2)}
		class="overflow-visible"
	>
		<path
			d="M {strokeWidth / 2} {radius}
				a {radius - strokeWidth / 2} {radius - strokeWidth / 2} 0 0 1 {normalizedRadius * 2} 0"
			fill="none"
			stroke="currentColor"
			stroke-width={strokeWidth}
			class="text-muted"
		/>
		<path
			d="M {strokeWidth / 2} {radius}
				a {radius - strokeWidth / 2} {radius - strokeWidth / 2} 0 0 1 {normalizedRadius * 2} 0"
			fill="none"
			stroke={arcColor}
			stroke-width={strokeWidth}
			stroke-linecap="round"
			class="transition-all duration-500 ease-out"
			style="stroke-dasharray: {circumference}; stroke-dashoffset: {strokeDashoffset};"
		/>
		<text
			x={radius + strokeWidth / 2}
			y={radius - 10}
			text-anchor="middle"
			class="fill-foreground text-4xl font-bold"
		>
			{score}
		</text>
	</svg>
	<Badge variant="outline" class="text-sm px-3 py-1">
		{rank}
	</Badge>
</div>
