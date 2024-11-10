<script setup lang="ts">
</script>

<template>
  <div id="tree"></div>
  <div id="main">
    <router-view></router-view>
  </div>
</template>

<style lang="scss" scoped>
#tree {
  flex: 1 20vw;
  height: 100vh;
  overflow: hidden;
  background-image: url("/sidebar.png");
  background-repeat: repeat-y;
}

#main {
  flex: 2 80vw;
  height: 100vh;
  overflow: auto;
  padding-left: 1rem;
}
</style>