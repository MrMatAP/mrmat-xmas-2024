<script setup lang="ts">
import { onMounted } from 'vue';
import { useAppInsights } from "../composables/useAppInsights.ts";
import { useStore } from "../composables/useStore.ts"

const { appInsights } = useAppInsights()
const { appState } = useStore()

onMounted(() => {
  appInsights.value.setAuthenticatedUserContext('stranger', 'stranger');
  appInsights.value.trackPageView({ name: 'stranger' })
  appState.isLoading = false
})
</script>

<template>
  <h1>Merry Christmas, Stranger</h1>
  <p>I'm afraid it's for invited guests only. I wish you a very happy Christmas anyway, or whatever it is that you may or may not be celebrating.</p>
</template>
