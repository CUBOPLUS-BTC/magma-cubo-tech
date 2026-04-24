<script lang="ts">
	type GeoState =
		| 'idle'
		| 'mining'
		| 'waiting'
		| 'success'
		| 'stacking'
		| 'sending'
		| 'studying'
		| 'hodl'
		| 'alert'
		| 'calculating'
		| 'nervous'
		| 'sleeping';

	let { state = 'idle', class: className = '' }: { state?: GeoState; class?: string } = $props();
</script>

{#if state === 'idle'}
	<svg viewBox="0 0 200 200" class="geo-float {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<g class="geo-tilt">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<ellipse cx="60" cy="135" rx="8" ry="4" fill="var(--geo-blush)" opacity="0.8"/>
			<ellipse cx="140" cy="135" rx="8" ry="4" fill="var(--geo-blush)" opacity="0.8"/>
			<g class="geo-blink">
				<circle cx="75" cy="122" r="9" fill="var(--geo-eye)" />
				<circle cx="125" cy="122" r="9" fill="var(--geo-eye)" />
				<circle cx="72" cy="119" r="3" fill="var(--geo-shine)" />
				<circle cx="122" cy="119" r="3" fill="var(--geo-shine)" />
			</g>
			<path d="M 90 132 Q 95 140 100 134 Q 105 140 110 132" fill="none" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 140 45 Q 145 60 145 75" stroke="rgba(255,255,255,0.4)" stroke-width="5" stroke-linecap="round" fill="none"/>
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			<circle cx="30" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="170" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" class="geo-wave-arm" />
		</g>
	</svg>

{:else if state === 'mining'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<path class="geo-spark-1" d="M 30 70 L 15 55 M 40 60 L 30 40" stroke="var(--geo-primary)" stroke-width="4" stroke-linecap="round" />
		<path class="geo-spark-2" d="M 170 70 L 185 55 M 160 60 L 170 40" stroke="var(--geo-primary)" stroke-width="4" stroke-linecap="round" />
		<g class="geo-vibrate">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 65 125 L 75 118 L 85 125 M 115 125 L 125 118 L 135 125" fill="none" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
			<path d="M 88 138 L 94 134 L 100 138 L 106 134 L 112 138" fill="none" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 140 45 Q 145 60 145 75" stroke="rgba(255,255,255,0.4)" stroke-width="5" stroke-linecap="round" fill="none"/>
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" class="geo-lamp-fast" />
			<circle cx="30" cy="120" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<g class="geo-pickaxe-swing">
				<path d="M 170 145 L 190 100" stroke="var(--geo-stroke)" stroke-width="8" stroke-linecap="round"/>
				<path d="M 180 105 Q 195 90 205 100 L 190 100 Q 175 90 180 105 Z" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="5" stroke-linejoin="round"/>
				<circle cx="170" cy="135" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			</g>
		</g>
	</svg>

{:else if state === 'waiting'}
	<svg viewBox="0 0 200 200" class="geo-float-slow {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<text x="145" y="90" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="16" class="geo-zzz-1">.</text>
		<text x="160" y="80" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="20" class="geo-zzz-2">.</text>
		<text x="175" y="70" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="24" class="geo-zzz-3">.</text>
		<g>
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 65 120 L 85 120 M 115 120 L 135 120" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<circle cx="75" cy="123" r="3" fill="var(--geo-eye)" />
			<circle cx="125" cy="123" r="3" fill="var(--geo-eye)" />
			<path d="M 95 138 L 105 138" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<g transform="rotate(3, 100, 80)">
				<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
				<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
				<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
				<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" opacity="0.3" />
			</g>
			<circle cx="45" cy="150" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="155" cy="150" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'success'}
	<svg viewBox="0 0 200 200" class="overflow-visible {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" class="geo-shadow-bounce" />
		<rect x="40" y="30" width="12" height="12" rx="4" fill="var(--geo-primary)" class="geo-confetti-1" />
		<circle cx="160" cy="40" r="6" fill="#34d399" class="geo-confetti-2" />
		<polygon points="80,10 90,25 70,25" fill="#60a5fa" class="geo-confetti-3" />
		<g class="geo-bounce">
			<path d="M 65 160 L 65 165 M 135 160 L 135 165" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 65 125 Q 75 112 85 125 M 115 125 Q 125 112 135 125" fill="none" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<ellipse cx="60" cy="130" rx="8" ry="4" fill="var(--geo-blush)" opacity="0.8"/>
			<ellipse cx="140" cy="130" rx="8" ry="4" fill="var(--geo-blush)" opacity="0.8"/>
			<path d="M 85 132 Q 100 160 115 132 Z" fill="var(--geo-eye)" stroke="var(--geo-stroke)" stroke-width="3" stroke-linejoin="round" />
			<path d="M 92 145 Q 100 152 108 145 Z" fill="var(--geo-blush)" />
			<g transform="translate(0, -8)">
				<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
				<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
				<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
				<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			</g>
			<circle cx="20" cy="90" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="180" cy="90" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'stacking'}
	<svg viewBox="0 0 200 200" class="geo-float {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<circle cx="55" cy="30" r="8" fill="#f59e0b" stroke="var(--geo-stroke)" stroke-width="2" class="geo-sat-fall-1" />
		<circle cx="145" cy="20" r="6" fill="#f59e0b" stroke="var(--geo-stroke)" stroke-width="2" class="geo-sat-fall-2" />
		<circle cx="100" cy="15" r="10" fill="#f59e0b" stroke="var(--geo-stroke)" stroke-width="3" class="geo-sat-fall-3" />
		<g class="geo-tilt">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="75" cy="120" r="15" fill="#f59e0b" stroke="var(--geo-stroke)" stroke-width="4" />
			<text x="75" y="128" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="20" fill="var(--geo-shine)">&#8383;</text>
			<circle cx="125" cy="120" r="15" fill="#f59e0b" stroke="var(--geo-stroke)" stroke-width="4" />
			<text x="125" y="128" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="20" fill="var(--geo-shine)">&#8383;</text>
			<path d="M 85 140 Q 100 152 115 140" fill="none" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 105 146 Q 110 155 115 145 Z" fill="var(--geo-blush)" stroke="var(--geo-stroke)" stroke-width="3" stroke-linejoin="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 140 45 Q 145 60 145 75" stroke="rgba(255,255,255,0.4)" stroke-width="5" stroke-linecap="round" fill="none"/>
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			<circle cx="90" cy="155" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" class="geo-rub-left" />
			<circle cx="110" cy="155" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" class="geo-rub-right" />
		</g>
	</svg>

{:else if state === 'sending'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="120" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<line x1="10" y1="100" x2="40" y2="100" stroke="var(--geo-stroke)" stroke-width="4" stroke-linecap="round" opacity="0.3" class="geo-speed-1" />
		<line x1="5" y1="130" x2="35" y2="130" stroke="var(--geo-stroke)" stroke-width="4" stroke-linecap="round" opacity="0.3" class="geo-speed-2" />
		<line x1="20" y1="160" x2="50" y2="160" stroke="var(--geo-stroke)" stroke-width="4" stroke-linecap="round" opacity="0.3" class="geo-speed-3" />
		<g class="geo-plane-fly">
			<path d="M 165 65 L 195 80 L 165 95 L 175 80 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="4" stroke-linejoin="round" />
		</g>
		<g transform="rotate(12, 100, 160)">
			<path d="M 65 160 L 50 170 M 135 160 L 145 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 65 115 L 85 122 M 135 115 L 115 122" fill="none" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<circle cx="78" cy="122" r="4" fill="var(--geo-eye)" />
			<circle cx="122" cy="122" r="4" fill="var(--geo-eye)" />
			<path d="M 92 138 L 108 138" fill="none" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			<circle cx="15" cy="110" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="185" cy="110" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'studying'}
	<svg viewBox="0 0 200 200" class="geo-float-slow {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<text x="150" y="50" font-family="sans-serif" font-size="20" font-weight="900" fill="var(--geo-stroke)" opacity="0.4" class="geo-thought-1">?</text>
		<text x="170" y="40" font-family="sans-serif" font-size="24" font-weight="900" fill="var(--geo-primary)" opacity="0.6" class="geo-thought-2">!</text>
		<g class="geo-tilt">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<line x1="85" y1="120" x2="115" y2="120" stroke="var(--geo-stroke)" stroke-width="5" />
			<circle cx="75" cy="120" r="16" fill="rgba(255,255,255,0.6)" stroke="var(--geo-stroke)" stroke-width="5" />
			<circle cx="125" cy="120" r="16" fill="rgba(255,255,255,0.6)" stroke="var(--geo-stroke)" stroke-width="5" />
			<path d="M 65 110 L 72 118 M 115 110 L 122 118" stroke="rgba(255,255,255,0.9)" stroke-width="4" stroke-linecap="round" />
			<circle cx="75" cy="120" r="3" fill="var(--geo-eye)" />
			<circle cx="125" cy="120" r="3" fill="var(--geo-eye)" />
			<circle cx="100" cy="140" r="4" fill="none" stroke="var(--geo-eye)" stroke-width="4" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			<circle cx="130" cy="155" r="10" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<g transform="translate(140, 140) rotate(-15)">
				<rect x="0" y="0" width="30" height="24" rx="4" fill="#8b5cf6" stroke="var(--geo-stroke)" stroke-width="4" />
				<line x1="15" y1="2" x2="15" y2="22" stroke="rgba(255,255,255,0.5)" stroke-width="2" />
			</g>
			<circle cx="30" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'hodl'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<g class="geo-sparkle-1"><polygon points="40,80 45,65 50,80 65,85 50,90 45,105 40,90 25,85" fill="#60a5fa" /></g>
		<g class="geo-sparkle-2"><polygon points="160,90 163,80 166,90 176,93 166,96 163,106 160,96 150,93" fill="#60a5fa" /></g>
		<g>
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<polygon points="75,108 88,122 75,136 62,122" fill="#60a5fa" stroke="var(--geo-stroke)" stroke-width="4" stroke-linejoin="round" />
			<polygon points="125,108 138,122 125,136 112,122" fill="#60a5fa" stroke="var(--geo-stroke)" stroke-width="4" stroke-linejoin="round" />
			<path d="M 60 105 L 85 110 M 140 105 L 115 110" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 85 145 L 115 145" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" />
			<rect x="50" y="140" width="60" height="24" rx="12" transform="rotate(15, 80, 150)" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="90" y="140" width="60" height="24" rx="12" transform="rotate(-15, 120, 150)" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'alert'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<line x1="30" y1="90" x2="10" y2="75" stroke="#ef4444" stroke-width="5" stroke-linecap="round" class="geo-impact-1" />
		<line x1="170" y1="90" x2="190" y2="75" stroke="#ef4444" stroke-width="5" stroke-linecap="round" class="geo-impact-2" />
		<line x1="25" y1="120" x2="5" y2="120" stroke="#ef4444" stroke-width="5" stroke-linecap="round" class="geo-impact-3" />
		<line x1="175" y1="120" x2="195" y2="120" stroke="#ef4444" stroke-width="5" stroke-linecap="round" class="geo-impact-4" />
		<g class="geo-vibrate">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="75" cy="120" r="16" fill="#ffffff" stroke="var(--geo-stroke)" stroke-width="5" />
			<circle cx="125" cy="120" r="16" fill="#ffffff" stroke="var(--geo-stroke)" stroke-width="5" />
			<circle cx="75" cy="120" r="4" fill="var(--geo-eye)" />
			<circle cx="125" cy="120" r="4" fill="var(--geo-eye)" />
			<ellipse cx="100" cy="145" rx="8" ry="12" fill="var(--geo-eye)" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="#ef4444" class="geo-lamp-alert" />
			<circle cx="20" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="180" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'calculating'}
	<svg viewBox="0 0 200 200" class="geo-float-slow {className}" xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<text x="30" y="60" font-family="sans-serif" font-size="16" font-weight="900" fill="var(--geo-stroke)" opacity="0.4" class="geo-num-1">21M</text>
		<text x="160" y="50" font-family="sans-serif" font-size="14" font-weight="900" fill="var(--geo-stroke)" opacity="0.4" class="geo-num-2">&#8383;</text>
		<text x="170" y="80" font-family="sans-serif" font-size="18" font-weight="900" fill="var(--geo-primary)" opacity="0.5" class="geo-num-3">%</text>
		<g class="geo-tilt">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="75" cy="120" r="10" fill="var(--geo-eye)" />
			<circle cx="72" cy="116" r="3" fill="var(--geo-shine)" />
			<path d="M 115 120 L 135 125" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<path d="M 60 102 L 85 98" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 90 138 L 110 138" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 95 138 L 95 146 Q 100 152 105 146 L 105 138 Z" fill="#f87171" stroke="var(--geo-stroke)" stroke-width="4" stroke-linejoin="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" class="geo-lamp-think" />
			<circle cx="30" cy="130" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="115" cy="155" r="10" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'nervous'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<g class="geo-shake">
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<path d="M 140 95 Q 150 110 140 115 Q 130 110 140 95 Z" fill="#60a5fa" stroke="var(--geo-stroke)" stroke-width="3" stroke-linejoin="round" class="geo-sweat-1" />
			<path d="M 45 105 Q 55 120 45 125 Q 35 120 45 105 Z" fill="#60a5fa" stroke="var(--geo-stroke)" stroke-width="3" stroke-linejoin="round" class="geo-sweat-2" />
			<circle cx="75" cy="122" r="12" fill="#ffffff" stroke="var(--geo-stroke)" stroke-width="4" />
			<circle cx="125" cy="122" r="12" fill="#ffffff" stroke="var(--geo-stroke)" stroke-width="4" />
			<circle cx="70" cy="120" r="4" fill="var(--geo-eye)" class="geo-dart-eyes" />
			<circle cx="120" cy="120" r="4" fill="var(--geo-eye)" class="geo-dart-eyes" />
			<path d="M 85 142 Q 90 137 95 142 T 105 142 T 115 142" fill="none" stroke="var(--geo-eye)" stroke-width="5" stroke-linecap="round" />
			<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" />
			<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" />
			<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="100" cy="66" r="8" fill="#f59e0b" opacity="0.5" />
			<circle cx="45" cy="135" r="10" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="155" cy="135" r="10" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>

{:else if state === 'sleeping'}
	<svg viewBox="0 0 200 200" class={className} xmlns="http://www.w3.org/2000/svg">
		<ellipse cx="100" cy="185" rx="45" ry="8" fill="var(--geo-shadow)" />
		<g>
			<path d="M 65 160 L 65 175 M 135 160 L 135 175" stroke="var(--geo-stroke)" stroke-width="12" stroke-linecap="round" />
			<rect x="40" y="75" width="120" height="90" rx="28" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<text x="140" y="90" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="14" class="geo-zzz-1" opacity="0.7">Z</text>
			<text x="155" y="70" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="20" class="geo-zzz-2" opacity="0.6">Z</text>
			<text x="175" y="45" fill="var(--geo-stroke)" font-family="sans-serif" font-weight="900" font-size="28" class="geo-zzz-3" opacity="0.5">Z</text>
			<path d="M 65 125 Q 75 135 85 125 M 115 125 Q 125 135 135 125" fill="none" stroke="var(--geo-eye)" stroke-width="6" stroke-linecap="round" />
			<circle cx="100" cy="140" r="3" fill="var(--geo-eye)" />
			<circle cx="112" cy="132" r="12" fill="rgba(255,255,255,0.9)" stroke="#94a3b8" stroke-width="3" class="geo-bubble" />
			<path d="M 116 126 A 5 5 0 0 1 120 132" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" class="geo-bubble" />
			<g transform="translate(0, 15) rotate(12, 100, 80)">
				<path d="M 40 85 C 40 25 160 25 160 85 Z" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" stroke-linejoin="round" opacity="0.95" />
				<rect x="30" y="80" width="140" height="14" rx="7" fill="var(--geo-primary)" stroke="var(--geo-stroke)" stroke-width="6" opacity="0.95" />
				<rect x="80" y="52" width="40" height="28" rx="8" fill="var(--geo-shine)" stroke="var(--geo-stroke)" stroke-width="6" />
				<circle cx="100" cy="66" r="8" fill="var(--lamp-light)" opacity="0.2" />
			</g>
			<circle cx="40" cy="140" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
			<circle cx="160" cy="140" r="12" fill="var(--geo-body)" stroke="var(--geo-stroke)" stroke-width="6" />
		</g>
	</svg>
{/if}

<style>
	/* Wrapper animations */
	.geo-float { animation: geo-float 3s ease-in-out infinite; }
	.geo-float-slow { animation: geo-float 4.5s ease-in-out infinite; }

	/* Body animations */
	.geo-tilt { animation: geo-tilt 6s ease-in-out infinite; transform-origin: 100px 180px; }
	.geo-vibrate { animation: geo-vibrate 0.15s linear infinite; transform-origin: 100px 180px; }
	.geo-bounce { animation: geo-bounce 1.5s cubic-bezier(0.28, 0.84, 0.42, 1) infinite; transform-origin: 100px 180px; }
	.geo-shadow-bounce { animation: geo-shadow-bounce 1.5s cubic-bezier(0.28, 0.84, 0.42, 1) infinite; transform-origin: 100px 185px; }
	.geo-shake { animation: geo-shake 0.4s ease-in-out infinite; transform-origin: 100px 180px; }

	/* Eyes */
	.geo-blink { animation: geo-blink 5s infinite; transform-box: fill-box; transform-origin: center; }
	.geo-dart-eyes { animation: geo-dart 2.5s ease-in-out infinite; }

	/* Arms */
	.geo-wave-arm { animation: geo-wave 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center bottom; }
	.geo-pickaxe-swing { animation: geo-swing 1s cubic-bezier(0.4, 0, 0.2, 1) infinite; transform-origin: 170px 135px; }

	/* Lamp */
	.geo-lamp-fast { animation: geo-lamp-fast 0.6s ease-in-out infinite; }
	.geo-lamp-alert { animation: geo-lamp-alert 0.3s cubic-bezier(1, 0, 0, 1) infinite; }
	.geo-lamp-think { animation: geo-lamp-think 2.5s ease-in-out infinite; }

	/* Sparks */
	.geo-spark-1 { animation: geo-spark 1.2s ease-out infinite; transform-origin: 35px 55px; }
	.geo-spark-2 { animation: geo-spark 1.4s ease-out infinite 0.4s; transform-origin: 165px 55px; }

	/* ZZZ */
	.geo-zzz-1 { animation: geo-zzz 2.5s ease-in infinite; }
	.geo-zzz-2 { animation: geo-zzz 2.5s ease-in infinite 0.8s; }
	.geo-zzz-3 { animation: geo-zzz 2.5s ease-in infinite 1.6s; }

	/* Confetti */
	.geo-confetti-1 { animation: geo-confetti 2s linear infinite; }
	.geo-confetti-2 { animation: geo-confetti 2.4s linear infinite 0.7s; }
	.geo-confetti-3 { animation: geo-confetti 1.8s linear infinite 0.3s; }

	/* Stacking */
	.geo-sat-fall-1 { animation: geo-sat-fall 2s ease-in infinite; }
	.geo-sat-fall-2 { animation: geo-sat-fall 2.5s ease-in infinite 0.8s; }
	.geo-sat-fall-3 { animation: geo-sat-fall 2.2s ease-in infinite 0.4s; }
	.geo-rub-left { animation: geo-rub-left 0.5s ease-in-out infinite alternate; }
	.geo-rub-right { animation: geo-rub-right 0.5s ease-in-out infinite alternate; }

	/* Sending */
	.geo-speed-1 { animation: geo-speed-line 0.6s linear infinite; }
	.geo-speed-2 { animation: geo-speed-line 0.8s linear infinite 0.2s; }
	.geo-speed-3 { animation: geo-speed-line 0.7s linear infinite 0.4s; }
	.geo-plane-fly { animation: geo-plane 2s ease-in-out infinite; }

	/* Studying */
	.geo-thought-1 { animation: geo-thought 3.5s ease-in-out infinite; }
	.geo-thought-2 { animation: geo-thought 4s ease-in-out infinite 1s; }

	/* HODL */
	.geo-sparkle-1 { animation: geo-sparkle 2.5s ease-in-out infinite; transform-origin: 45px 85px; }
	.geo-sparkle-2 { animation: geo-sparkle 3s ease-in-out infinite 0.5s; transform-origin: 163px 93px; }

	/* Alert */
	.geo-impact-1, .geo-impact-2, .geo-impact-3, .geo-impact-4 { animation: geo-impact 0.5s ease-out infinite alternate; }
	.geo-impact-2 { animation-delay: 0.1s; }
	.geo-impact-3 { animation-delay: 0.2s; }
	.geo-impact-4 { animation-delay: 0.3s; }

	/* Calculating */
	.geo-num-1 { animation: geo-num-float 4s ease-in-out infinite; }
	.geo-num-2 { animation: geo-num-float 4.5s ease-in-out infinite 0.7s; }
	.geo-num-3 { animation: geo-num-float 3.8s ease-in-out infinite 1.2s; }

	/* Nervous */
	.geo-sweat-1 { animation: geo-sweat 1.5s ease-in infinite; }
	.geo-sweat-2 { animation: geo-sweat 1.8s ease-in infinite 0.6s; }

	/* Sleeping */
	.geo-bubble { animation: geo-bubble 4s ease-in-out infinite; transform-box: fill-box; transform-origin: left bottom; }

	/* --- Keyframes --- */
	@keyframes geo-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
	@keyframes geo-tilt { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(4deg); } 75% { transform: rotate(-4deg); } }
	@keyframes geo-vibrate { 0%, 100% { transform: translate(0, 0) rotate(0deg); } 25% { transform: translate(-2px, -2px) rotate(-1deg); } 50% { transform: translate(2px, 0px) rotate(1deg); } 75% { transform: translate(-1px, 2px) rotate(0deg); } }
	@keyframes geo-bounce { 0%, 100% { transform: scaleY(1) translateY(0); } 40% { transform: scaleY(0.9) translateY(15px); } 50% { transform: scaleY(1.1) translateY(-20px); } 70% { transform: scaleY(0.95) translateY(5px); } }
	@keyframes geo-shadow-bounce { 0%, 100% { transform: scaleX(1); opacity: 1; } 40% { transform: scaleX(1.2); opacity: 0.7; } 50% { transform: scaleX(0.7); opacity: 0.4; } }
	@keyframes geo-shake { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(2deg); } 75% { transform: rotate(-2deg); } }
	@keyframes geo-blink { 0%, 94%, 98%, 100% { transform: scaleY(1); } 96% { transform: scaleY(0); } }
	@keyframes geo-dart { 0%, 100% { transform: translateX(0); } 25%, 45% { transform: translateX(-4px); } 55%, 75% { transform: translateX(4px); } }
	@keyframes geo-wave { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(40deg); } }
	@keyframes geo-swing { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(-50deg); } }
	@keyframes geo-lamp-fast { 0%, 100% { opacity: 1; filter: drop-shadow(0 0 10px var(--lamp-light)); } 50% { opacity: 0.6; filter: none; } }
	@keyframes geo-lamp-alert { 0%, 49% { fill: #ef4444; filter: drop-shadow(0 0 15px #ef4444); } 50%, 100% { fill: #7f1d1d; filter: none; } }
	@keyframes geo-lamp-think { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; filter: drop-shadow(0 0 8px #fff); } }
	@keyframes geo-spark { 0% { transform: scale(0.5); opacity: 0; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(0); opacity: 0; } }
	@keyframes geo-zzz { 0% { transform: translate(0, 0) scale(0.5); opacity: 0; } 50% { opacity: 1; } 100% { transform: translate(15px, -25px) scale(1.5); opacity: 0; } }
	@keyframes geo-confetti { 0% { transform: translateY(-20px) rotate(0deg); opacity: 1; } 100% { transform: translateY(120px) rotate(360deg); opacity: 0; } }
	@keyframes geo-sat-fall { 0% { transform: translateY(-30px) rotate(0deg); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(150px) rotate(180deg); opacity: 0; } }
	@keyframes geo-rub-left { 0% { transform: translate(-3px, -3px); } 100% { transform: translate(3px, 3px); } }
	@keyframes geo-rub-right { 0% { transform: translate(3px, -3px); } 100% { transform: translate(-3px, 3px); } }
	@keyframes geo-speed-line { 0% { transform: translateX(30px); opacity: 0; } 50% { opacity: 0.4; } 100% { transform: translateX(-50px); opacity: 0; } }
	@keyframes geo-plane { 0%, 100% { transform: translate(0, 0) rotate(0deg); } 50% { transform: translate(10px, -5px) rotate(5deg); } }
	@keyframes geo-thought { 0%, 100% { transform: scale(0.9); opacity: 0.3; } 50% { transform: scale(1.2); opacity: 0.8; } }
	@keyframes geo-sparkle { 0%, 100% { transform: scale(0); opacity: 0; } 50% { transform: scale(1); opacity: 1; } }
	@keyframes geo-impact { 0% { transform: scaleX(0.8); opacity: 0.5; } 100% { transform: scaleX(1.2); opacity: 1; } }
	@keyframes geo-num-float { 0%, 100% { transform: translateY(0); opacity: 0.3; } 50% { transform: translateY(-10px); opacity: 0.6; } }
	@keyframes geo-sweat { 0% { transform: translateY(-5px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translateY(20px); opacity: 0; } }
	@keyframes geo-bubble { 0%, 100% { transform: scale(0.8); opacity: 0.6; } 50% { transform: scale(1.3); opacity: 1; } }
</style>
