<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { auth } from '$lib/stores/auth.svelte';

  if (browser) {
    goto(auth.isAuthenticated ? '/home' : '/login', { replaceState: true });
  }
</script>
