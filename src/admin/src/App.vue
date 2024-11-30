<script setup lang="ts">
import { useAuth, msal } from "./composables/useAuth.ts";
import { useCosmos } from "./composables/useCosmos.ts"
import { useXmasStore } from "./stores/useXmasStore.ts";
import { onMounted } from "vue";

const { handleRedirect } = useAuth();
const { cosmosLogin } = useCosmos();
const store = useXmasStore();

onMounted(async () => {
  try {
    await msal.initialize();
    await cosmosLogin();
    await store.list()
  } catch (error) {
    console.error('Initialisation error', error)
  }
  await handleRedirect();
})
</script>

<template>
  <router-view/>
</template>

<style lang="sass">
#app
  background-color: $secondary
</style>