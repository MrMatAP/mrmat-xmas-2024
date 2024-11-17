<script setup lang="ts">
import { useAuth, myMSALObj } from "./composables/useAuth.ts";
import { useCosmos } from "./composables/useCosmos.ts"
import { useBlob } from './composables/useBlob.ts'
import { useXmasStore } from "./stores/useXmasStore.ts";
import { onMounted } from "vue";

const { handleRedirect } = useAuth();
const { cosmosLogin } = useCosmos();
const { blobLogin } = useBlob();
const store = useXmasStore();

onMounted(async () => {
  try {
    await myMSALObj.initialize();
    await cosmosLogin();
    await blobLogin();
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