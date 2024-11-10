<script setup lang="ts">
import AppLoading from "./components/AppLoading.vue";
import AppError from "./components/AppError.vue";
</script>

<template>
  <router-view/>
  <AppLoading/>
  <AppError/>
</template>
