<script setup lang="ts">
import { useStore } from '../composables/useStore.ts'

const { appState } = useStore()
</script>

<template>
  <div class="overlay" v-show="appState.isLoading">
    <div class="loader"></div>
  </div>
</template>
