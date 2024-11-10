<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { useStore } from "../composables/useStore.ts"

const $router = useRouter()
const $route = useRoute()
const { appState, person, getUser } = useStore()

onMounted( async () => {
  appState.isLoading = true;
  const uid = $route.params.uid
  await getUser(uid as string);
  if(person.value.id == "0") {
    await $router.push({name: 'Stranger'});
  } else {
    await $router.push({name: 'Main'});
  }
  appState.isLoading = false;
})
</script>

<template>
  
</template>

<style scoped>

</style>