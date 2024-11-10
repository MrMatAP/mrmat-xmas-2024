<script setup lang="ts">
import { onMounted } from 'vue';
import { useStore } from "../composables/useStore.ts"

const { appState } = useStore()

onMounted(() => {
  appState.isLoading = false
})
</script>

<template>
  <h1>Merry Christmas, Stranger</h1>
  <p>I'm afraid it's for invited guests only. I wish you a very happy Christmas anyway, or whatever it is that you may or may not be celebrating.</p>
</template>
