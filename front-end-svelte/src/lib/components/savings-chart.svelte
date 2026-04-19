<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
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

	let canvas: HTMLCanvasElement;
	let chart: any = null;

	const chartData = $derived(
		data.map((d) => ({
			month: d.month,
			invested: d.invested,
			traditional: 'traditional' in d ? d.traditional : d.traditional_value,
			btc: 'btc_moderate' in d ? d.btc_moderate : d.btc_value,
		}))
	);

	async function createChart() {
		if (!browser || !canvas) return;

		const { Chart, registerables } = await import('chart.js');
		Chart.register(...registerables);

		if (chart) chart.destroy();

		const labels = chartData.map((d) =>
			d.month % 12 === 0 ? `${d.month / 12}yr` : ''
		);

		const style = getComputedStyle(document.documentElement);
		const mutedFg = style.getPropertyValue('--muted-foreground').trim();
		const borderColor = style.getPropertyValue('--border').trim();

		const ctx = canvas.getContext('2d')!;

		const btcGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
		btcGradient.addColorStop(0, 'rgba(16, 185, 129, 0.30)');
		btcGradient.addColorStop(1, 'rgba(16, 185, 129, 0.02)');

		const tradGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
		tradGradient.addColorStop(0, 'rgba(99, 102, 241, 0.20)');
		tradGradient.addColorStop(1, 'rgba(99, 102, 241, 0.02)');

		chart = new Chart(ctx, {
			type: 'line',
			data: {
				labels,
				datasets: [
					{
						label: 'Bitcoin DCA',
						data: chartData.map((d) => d.btc),
						borderColor: '#10b981',
						backgroundColor: btcGradient,
						borderWidth: 2.5,
						fill: true,
						tension: 0.4,
						pointRadius: 0,
						pointHoverRadius: 5,
						pointHoverBackgroundColor: '#10b981',
						pointHoverBorderColor: '#fff',
						pointHoverBorderWidth: 2,
					},
					{
						label: 'Traditional 2%',
						data: chartData.map((d) => d.traditional),
						borderColor: '#6366f1',
						backgroundColor: tradGradient,
						borderWidth: 1.5,
						fill: true,
						tension: 0.4,
						pointRadius: 0,
						pointHoverRadius: 4,
						pointHoverBackgroundColor: '#6366f1',
						pointHoverBorderColor: '#fff',
						pointHoverBorderWidth: 2,
					},
					{
						label: 'Invested',
						data: chartData.map((d) => d.invested),
						borderColor: 'rgba(140, 140, 160, 0.5)',
						backgroundColor: 'transparent',
						borderWidth: 1.5,
						borderDash: [6, 4],
						fill: false,
						tension: 0,
						pointRadius: 0,
						pointHoverRadius: 3,
					},
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				interaction: {
					mode: 'index',
					intersect: false,
				},
				plugins: {
					legend: {
						position: 'bottom',
						labels: {
							color: 'oklch(0.60 0.01 260)',
							usePointStyle: true,
							pointStyle: 'circle',
							padding: 20,
							font: { size: 12, family: 'DM Sans Variable, sans-serif' },
						},
					},
					tooltip: {
						backgroundColor: 'oklch(0.185 0.007 260 / 95%)',
						titleColor: 'oklch(0.93 0.008 80)',
						bodyColor: 'oklch(0.93 0.008 80)',
						borderColor: 'oklch(1 0.005 260 / 15%)',
						borderWidth: 1,
						cornerRadius: 12,
						padding: 12,
						titleFont: { size: 13, family: 'Space Grotesk Variable, sans-serif', weight: '600' as any },
						bodyFont: { size: 12, family: 'DM Sans Variable, sans-serif' },
						displayColors: true,
						usePointStyle: true,
						callbacks: {
							title: (items: any[]) => {
								const month = chartData[items[0].dataIndex]?.month;
								if (!month) return '';
								return month % 12 === 0
									? `Year ${month / 12}`
									: `Month ${month}`;
							},
							label: (item: any) => {
								const val = item.raw as number;
								return ` ${item.dataset.label}: $${val >= 1000 ? val.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) : val.toFixed(2)}`;
							},
						},
					},
				},
				scales: {
					x: {
						grid: { display: false },
						ticks: {
							color: 'oklch(0.60 0.01 260)',
							font: { size: 11, family: 'DM Sans Variable, sans-serif' },
							maxRotation: 0,
							autoSkip: true,
							maxTicksLimit: 8,
						},
						border: { display: false },
					},
					y: {
						grid: {
							color: 'oklch(1 0.005 260 / 8%)',
						},
						ticks: {
							color: 'oklch(0.60 0.01 260)',
							font: { size: 11, family: 'DM Sans Variable, sans-serif' },
							callback: (v: any) => {
								const val = Number(v);
								if (val >= 1_000_000) return `$${(val / 1_000_000).toFixed(1)}M`;
								if (val >= 1000) return `$${(val / 1000).toFixed(0)}K`;
								return `$${val}`;
							},
						},
						border: { display: false },
					},
				},
			},
		});
	}

	onMount(() => {
		createChart();
		return () => { if (chart) chart.destroy(); };
	});

	$effect(() => {
		if (chartData && browser && canvas) createChart();
	});
</script>

<Card>
	<CardHeader class="pb-2">
		<CardTitle class="font-heading text-base font-semibold">
			{i18n.t.savings.projectionTitle ?? 'Growth Over Time'}
		</CardTitle>
	</CardHeader>
	<CardContent class="pt-0">
		<div class="h-[320px]">
			<canvas bind:this={canvas}></canvas>
		</div>
	</CardContent>
</Card>
