<script setup lang="ts">
import { computed } from 'vue';
import { useStore } from '../composables/useStore.ts'

const { appState } = useStore()

const errorMessageId = computed(() => {
  return 'errorMessages.' + appState.errorMessageId
})
</script>

<template>
<div class="overlay" v-show="appState.isError">
  <div class="errorMessage">
    <h1>{{ $t('errorHeader')}}</h1>
    <p>{{ $t(errorMessageId) }}</p>
  </div>
</div>
</template>
