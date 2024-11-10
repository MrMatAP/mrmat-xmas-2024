<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from './composables/useStore.ts'
import AppLoading from "./components/AppLoading.vue";
import AppError from "./components/AppError.vue";

const $router = useRouter()
const $route = useRoute()
const { initialise, appState, identity } = useStore()

onMounted(async () => {
  appState.isLoading = true;
  const uid = $route.params.uid
  await initialise(uid);
  if(identity.value.id !== "0") {
    await $router.push({name: 'Identified'})
  } else {
    await $router.push({ name: 'Stranger'})
  }
  appState.isLoading = false;
})
</script>

<template>
  <router-view/>
  <AppLoading/>
  <AppError/>
</template>

<style scoped>
</style>
