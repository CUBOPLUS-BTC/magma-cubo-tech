<script lang="ts">
	import { AreaChart } from 'layerchart';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { i18n } from '$lib/i18n/index.svelte';

	interface SavingsDataPoint {
		month: number;
		invested: number;
		traditional: number;
		btc_moderate: number;
	}

	interface PensionDataPoint {
		month: number;
		invested: number;
		traditional_value: number;
		btc_value: number;
	}

	type MonthlyDataPoint = SavingsDataPoint | PensionDataPoint;

	let { data }: { data: MonthlyDataPoint[] } = $props();

	let chartData = $derived(
		data.map((d) => ({
			month: d.month,
			invested: d.invested,
			traditional: 'traditional' in d ? d.traditional : d.traditional_value,
			btc: 'btc_moderate' in d ? d.btc_moderate : d.btc_value,
		}))
	);
</script>

<Card>
	<CardHeader class="pb-2">
		<CardTitle class="font-heading text-base font-semibold">
			{i18n.t.savings.projectionTitle ?? 'Growth Over Time'}
		</CardTitle>
	</CardHeader>
	<CardContent class="pt-0">
		<div class="h-[300px]">
			<AreaChart
				data={chartData}
				x="month"
				series={[
					{
						key: 'invested',
						label: 'Invested',
						color: 'oklch(0.60 0.01 260)',
						props: { fill: 'oklch(0.60 0.01 260 / 8%)', strokeDasharray: '6,4' },
					},
					{
						key: 'traditional',
						label: 'Traditional 2%',
						color: 'oklch(0.60 0.15 55)',
						props: { fill: 'oklch(0.60 0.15 55 / 10%)' },
					},
					{
						key: 'btc',
						label: 'Bitcoin DCA',
						color: 'oklch(0.70 0.20 38)',
						props: { fill: 'oklch(0.70 0.20 38 / 15%)' },
					},
				]}
				seriesLayout="overlap"
				legend
				props={{
					xAxis: {
						format: (v: number) => (v % 12 === 0 ? `${v / 12}yr` : `${v}mo`),
					},
					yAxis: {
						format: (v: number) =>
							v >= 1_000_000
								? `$${(v / 1_000_000).toFixed(1)}M`
								: v >= 1000
									? `$${(v / 1000).toFixed(0)}K`
									: `$${v}`,
					},
				}}
			/>
		</div>
	</CardContent>
</Card>
