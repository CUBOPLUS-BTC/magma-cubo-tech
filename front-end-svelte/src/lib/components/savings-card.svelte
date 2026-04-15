<script lang="ts">
	import { formatUSD } from '$lib/utils/formatters';
	import { Card } from '$lib/components/ui/card';
	import { CardHeader } from '$lib/components/ui/card';
	import { CardTitle } from '$lib/components/ui/card';
	import { CardContent } from '$lib/components/ui/card';

	let {
		annualSavings,
		bestChannel
	}: {
		annualSavings: number;
		bestChannel: string;
	} = $props();

	let monthlySavings = $derived(annualSavings / 12);
</script>

<Card class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950/30 dark:to-green-900/20 border-green-200 dark:border-green-800">
	<CardHeader>
		<CardTitle class="text-muted-foreground">Potential Annual Savings</CardTitle>
	</CardHeader>

	<CardContent class="space-y-4">
		<div class="text-4xl font-bold text-green-600 dark:text-green-500">
			{formatUSD(annualSavings)}
		</div>

		<div class="space-y-1">
			<p class="text-sm text-muted-foreground">
				vs worst channel with <span class="font-medium text-foreground">{bestChannel}</span>
			</p>
			<p class="text-lg font-medium text-green-700 dark:text-green-400">
				{formatUSD(monthlySavings)}/month
			</p>
		</div>
	</CardContent>
</Card>
