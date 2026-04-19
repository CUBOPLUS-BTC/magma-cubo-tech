<script lang="ts">
	import { onMount } from "svelte";
	import { cn } from "$lib/utils";

	interface NumberTickerProps {
		value: number;
		startValue?: number;
		direction?: "up" | "down";
		delay?: number;
		decimalPlaces?: number;
		class?: string;
	}

	let {
		value,
		startValue = 0,
		direction = "up",
		delay = 0,
		decimalPlaces = 0,
		class: className,
	}: NumberTickerProps = $props();

	let spanRef: HTMLSpanElement | null = $state(null);

	function animateValue(from: number, to: number) {
		let velocity = 0;
		let position = from;
		const target = to;
		const damping = 60;
		const stiffness = 100;
		const startTime = performance.now();

		function step(currentTime: number) {
			const elapsed = currentTime - startTime;
			const dt = 16.67 / 1000;
			const springForce = -stiffness * (position - target);
			const dampingForce = -damping * velocity;
			velocity += (springForce + dampingForce) * dt;
			position += velocity * dt;

			if (spanRef) {
				spanRef.textContent = Intl.NumberFormat("en-US", {
					minimumFractionDigits: decimalPlaces,
					maximumFractionDigits: decimalPlaces,
				}).format(Number(position.toFixed(decimalPlaces)));
			}

			const isSettled = Math.abs(velocity) < 0.01 && Math.abs(position - target) < 0.01;
			if (!isSettled && elapsed < 4000) {
				requestAnimationFrame(step);
			} else if (spanRef) {
				spanRef.textContent = Intl.NumberFormat("en-US", {
					minimumFractionDigits: decimalPlaces,
					maximumFractionDigits: decimalPlaces,
				}).format(Number(target.toFixed(decimalPlaces)));
			}
		}

		requestAnimationFrame(step);
	}

	onMount(() => {
		if (!spanRef) return;

		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting) {
					setTimeout(() => {
						const from = direction === "down" ? value : startValue;
						const to = direction === "down" ? startValue : value;
						animateValue(from, to);
					}, delay * 1000);
					observer.disconnect();
				}
			},
			{ threshold: 0.1 }
		);

		observer.observe(spanRef);
		return () => observer.disconnect();
	});
</script>

<span
	bind:this={spanRef}
	class={cn("inline-block tabular-nums", className)}
>
	{Intl.NumberFormat("en-US", {
		minimumFractionDigits: decimalPlaces,
		maximumFractionDigits: decimalPlaces,
	}).format(Number((direction === "down" ? value : startValue).toFixed(decimalPlaces)))}
</span>
