<script setup lang="ts">
</script>

<template>
  <div id="tree">
    <canvas id="ctree"></canvas>
  </div>
  <div id="main">
    <router-view></router-view>
  </div>
</template>

<style lang="scss" scoped>
#tree {
  flex: 1 20vw;
  height: 100vh;
  overflow: hidden;
}

#ctree {
  width: 100%;
  height: 100%;
}

#main {
  flex: 2 80vw;
  height: 100vh;
  overflow: auto;
}
</style>