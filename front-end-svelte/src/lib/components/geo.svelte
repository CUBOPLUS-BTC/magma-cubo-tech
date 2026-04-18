<script lang="ts">
	type GeoState = 'idle' | 'mining' | 'waiting' | 'success';

	let { state = 'idle', class: className = '' }: { state?: GeoState; class?: string } = $props();
</script>

{#if state === 'idle'}
	<!-- Idle / Saludando -->
	<svg viewBox="0 0 200 200" class="geo-float {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="180" rx="35" ry="6" fill="var(--geo-shadow)" />

		<g class="geo-tilt">
			<rect x="45" y="80" width="110" height="90" rx="16" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="4" />

			<path d="M 55 155 L 70 155 L 75 165" fill="none" stroke="var(--geo-stroke)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
			<path d="M 145 155 L 130 155 L 125 165" fill="none" stroke="var(--geo-stroke)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

			<g class="geo-blink">
				<ellipse cx="75" cy="125" rx="7" ry="11" fill="var(--geo-eye)" />
				<ellipse cx="125" cy="125" rx="7" ry="11" fill="var(--geo-eye)" />
				<circle cx="72" cy="120" r="2.5" fill="var(--geo-shine)" />
				<circle cx="122" cy="120" r="2.5" fill="var(--geo-shine)" />
			</g>

			<ellipse cx="58" cy="135" rx="7" ry="4" fill="var(--geo-blush)" />
			<ellipse cx="142" cy="135" rx="7" ry="4" fill="var(--geo-blush)" />
			<path d="M 92 133 Q 100 142 108 133" stroke="var(--geo-eye)" stroke-width="3.5" fill="none" stroke-linecap="round" />

			<rect x="35" y="70" width="130" height="12" rx="6" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
			<path d="M 50 72 C 50 30 150 30 150 72 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
			<path d="M 100 35 L 100 70" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round" />
			<path d="M 75 42 L 75 70" stroke="rgba(255,255,255,0.25)" stroke-width="3" stroke-linecap="round" />
			<path d="M 125 42 L 125 70" stroke="rgba(255,255,255,0.25)" stroke-width="3" stroke-linecap="round" />

			<rect x="85" y="50" width="30" height="24" rx="4" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="2" />
			<circle cx="100" cy="62" r="8" fill="var(--lamp-light)" style="filter: var(--lamp-glow);" />
		</g>
	</svg>

{:else if state === 'mining'}
	<!-- Mining / Minando -->
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="180" rx="35" ry="6" fill="var(--geo-shadow)" />

		<path class="geo-spark-1" d="M 50 80 L 45 70 M 55 75 L 60 65" stroke="var(--geo-primary)" stroke-width="3" stroke-linecap="round" />
		<path class="geo-spark-2" d="M 150 80 L 155 70 M 145 75 L 140 65" stroke="var(--geo-primary)" stroke-width="3" stroke-linecap="round" />

		<g class="geo-vibrate">
			<rect x="45" y="80" width="110" height="90" rx="16" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="4" />

			<path d="M 68 120 L 80 128" stroke="var(--geo-eye)" stroke-width="4" stroke-linecap="round" />
			<path d="M 132 120 L 120 128" stroke="var(--geo-eye)" stroke-width="4" stroke-linecap="round" />

			<ellipse cx="58" cy="135" rx="8" ry="5" fill="var(--geo-blush)" />
			<ellipse cx="142" cy="135" rx="8" ry="5" fill="var(--geo-blush)" />

			<path d="M 90 138 Q 100 135 110 138" stroke="var(--geo-eye)" stroke-width="3" fill="none" stroke-linecap="round" />

			<rect x="35" y="70" width="130" height="12" rx="6" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
			<path d="M 50 72 C 50 30 150 30 150 72 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
			<path d="M 100 35 L 100 70" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round" />

			<rect x="85" y="50" width="30" height="24" rx="4" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="2" />
			<circle cx="100" cy="62" r="8" fill="var(--lamp-light)" class="geo-lamp-fast" />
		</g>
	</svg>

{:else if state === 'waiting'}
	<!-- Waiting / Esperando -->
	<svg viewBox="0 0 200 200" class="geo-float-slow {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="180" rx="35" ry="6" fill="var(--geo-shadow)" />

		<g>
			<rect x="45" y="80" width="110" height="90" rx="16" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="4" />

			<text x="145" y="90" fill="var(--geo-stroke)" font-family="Space Grotesk" font-weight="bold" font-size="16" class="geo-zzz-1">z</text>
			<text x="160" y="70" fill="var(--geo-stroke)" font-family="Space Grotesk" font-weight="bold" font-size="22" class="geo-zzz-2">Z</text>

			<path d="M 68 125 L 82 125" stroke="var(--geo-eye)" stroke-width="4" stroke-linecap="round" />
			<path d="M 118 125 L 132 125" stroke="var(--geo-eye)" stroke-width="4" stroke-linecap="round" />

			<circle cx="105" cy="132" r="6" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="2" />
			<circle cx="95" cy="135" r="2.5" fill="var(--geo-eye)" />

			<g transform="rotate(3, 100, 70)">
				<rect x="35" y="70" width="130" height="12" rx="6" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" opacity="0.95" />
				<path d="M 50 72 C 50 30 150 30 150 72 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" opacity="0.95" />
				<path d="M 100 35 L 100 70" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round" />

				<rect x="85" y="50" width="30" height="24" rx="4" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="2" />
				<circle cx="100" cy="62" r="8" fill="var(--lamp-light)" opacity="0.3" />
			</g>
		</g>
	</svg>

{:else if state === 'success'}
	<!-- Success / Éxito -->
	<svg viewBox="0 0 200 200" class="overflow-visible {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="180" rx="35" ry="6" fill="var(--geo-shadow)" />

		<rect x="40" y="30" width="8" height="8" rx="2" fill="var(--geo-primary)" class="geo-confetti-1" />
		<rect x="160" y="50" width="6" height="6" rx="1" fill="#fbbf24" class="geo-confetti-2" />
		<rect x="80" y="20" width="10" height="10" rx="2" fill="var(--geo-primary)" class="geo-confetti-3" />

		<g class="geo-bounce">
			<rect x="45" y="80" width="110" height="90" rx="16" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="4" />

			<path d="M 68 125 Q 75 115 82 125" stroke="var(--geo-eye)" stroke-width="4" fill="none" stroke-linecap="round" />
			<path d="M 118 125 Q 125 115 132 125" stroke="var(--geo-eye)" stroke-width="4" fill="none" stroke-linecap="round" />

			<ellipse cx="58" cy="130" rx="8" ry="5" fill="var(--geo-blush)" />
			<ellipse cx="142" cy="130" rx="8" ry="5" fill="var(--geo-blush)" />

			<path d="M 85 133 Q 100 150 115 133 Z" fill="var(--geo-eye)" />

			<g transform="translate(0, -5)">
				<rect x="35" y="70" width="130" height="12" rx="6" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
				<path d="M 50 72 C 50 30 150 30 150 72 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="2" />
				<path d="M 100 35 L 100 70" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round" />

				<rect x="85" y="50" width="30" height="24" rx="4" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="2" />
				<circle cx="100" cy="62" r="8" fill="var(--lamp-light)" style="filter: var(--lamp-glow);" />
			</g>
		</g>
	</svg>
{/if}

<style>
	/* Wrapper animations */
	.geo-float { animation: geo-float 3s ease-in-out infinite; }
	.geo-float-slow { animation: geo-float-slow 4s ease-in-out infinite; }

	/* Body animations */
	.geo-tilt { animation: geo-tilt 6s ease-in-out infinite; transform-origin: bottom center; }
	.geo-vibrate { animation: geo-vibrate 0.2s linear infinite; }
	.geo-bounce { animation: geo-bounce 2s cubic-bezier(0.28, 0.84, 0.42, 1) infinite; transform-origin: bottom center; }

	/* Eyes */
	.geo-blink { animation: geo-blink 4.5s infinite; transform-box: fill-box; transform-origin: center; }

	/* Lamp */
	.geo-lamp-fast { animation: geo-lamp-fast 0.5s ease-in-out infinite; }

	/* Sparks */
	.geo-spark-1 { animation: geo-spark 1s ease-out infinite; transform-origin: center; }
	.geo-spark-2 { animation: geo-spark 1.2s ease-out infinite 0.3s; transform-origin: center; }

	/* ZZZ */
	.geo-zzz-1 { animation: geo-zzz 2s ease-in infinite; }
	.geo-zzz-2 { animation: geo-zzz 2.5s ease-in infinite 1s; }

	/* Confetti */
	.geo-confetti-1 { animation: geo-confetti 1.5s linear infinite; }
	.geo-confetti-2 { animation: geo-confetti 1.8s linear infinite 0.5s; }
	.geo-confetti-3 { animation: geo-confetti 1.6s linear infinite 0.2s; }
</style>
