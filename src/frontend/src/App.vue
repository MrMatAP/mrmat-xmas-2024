<script setup lang="ts">
import { onMounted } from 'vue';
import { useAppInsights } from "./composables/useAppInsights.ts";
import AppLoading from "./components/AppLoading.vue";
import AppError from "./components/AppError.vue";

const { appInsights } = useAppInsights()

onMounted( () => {
  appInsights.value.loadAppInsights();
})
</script>

<template>
  <router-view/>
  <AppLoading/>
  <AppError/>
</template>
