<script lang="ts">
	import type { ChannelComparison } from '$lib/models/remittance';
	import { formatUSD } from '$lib/utils/formatters';
	import { Card } from '$lib/components/ui/card';
	import { CardHeader } from '$lib/components/ui/card';
	import { CardTitle } from '$lib/components/ui/card';
	import { CardDescription } from '$lib/components/ui/card';
	import { CardContent } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';

	let { channel }: { channel: ChannelComparison } = $props();
</script>

<Card
	class="relative border-l-4 {channel.is_recommended
		? 'border-l-primary'
		: 'border-l-transparent'}"
>
	{#if channel.is_recommended}
		<Badge class="absolute -top-2 right-2 bg-primary text-primary-foreground">RECOMMENDED</Badge>
	{/if}

	<CardHeader>
		<CardTitle class="text-base">{channel.name}</CardTitle>
		<CardDescription class="flex items-center gap-2">
			<span>Fee:</span>
			<span class="font-medium text-foreground">{channel.fee_percent}%</span>
		</CardDescription>
	</CardHeader>

	<CardContent class="space-y-3">
		<div class="flex justify-between items-center">
			<span class="text-sm text-muted-foreground">Amount Received</span>
			<span class="text-lg font-semibold text-green-600 dark:text-green-500">
				{formatUSD(channel.amount_received)}
			</span>
		</div>

		<div class="flex justify-between items-center">
			<span class="text-sm text-muted-foreground">Estimated Time</span>
			<span class="text-sm font-medium">{channel.estimated_time}</span>
		</div>
	</CardContent>
</Card>
