<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from "../composables/useStore.ts"

const $router = useRouter()
const { appState, person, pictureUrl, getUser, updateUser, updatePicture } = useStore()

const fileSelector = ref()
const uploading = ref(false);

async function onSend() {
  uploading.value = true;
  await updateUser();
  uploading.value = false;
}

function onSelectPicture() {
  fileSelector.value.click();
}

async function onPictureSelected() {
  const localImage = fileSelector.value.files[0]
  uploading.value = true;
  await updatePicture(localImage);
  uploading.value = false;
}

onMounted( async () => {
  appState.isLoading = true;
  await getUser(undefined);
  if(person.value.id == "0") await $router.push({name: 'Stranger'});
  appState.isLoading = false;
})
</script>

<template>
  <h1>{{ person.greeting }} {{ person.name }}</h1>
  <p>
    My analogue engineering challenge for you this year is to bake a cake in the general theme of the season (or some
    jelly, if you live in a warmer climate). The silicone mould I'm sending along is good for temperatures between -60C
    to 230C and it does get along with dishwashers. I'm afraid I can give you just one of these tree-shaped moulds,
    so take the opportunity to make some cookies as well.
  </p>
  <p>
    Whatever you do, send me a note along with a picture of yourself enjoying the results.
  </p>

  <div class="form">
    <div class="imagePlaceholder">
      <img v-show="!uploading" :src="pictureUrl" alt="Your image" @click="onSelectPicture">
    </div>
    <textarea v-model="person.message" autofocus maxlength="1000"></textarea>
    <div class="operations">
      <div v-show="! uploading">
        <input ref="fileSelector" type="file" @change.prevent="onPictureSelected" style="display: none"/>
        <button @click.prevent="onSend" :disabled="uploading">Send</button>
      </div>
    </div>

    <div v-show="uploading" class="overlay">
      <div class="loader"></div>
    </div>
  </div>
</template>

<style lang="scss">

</style>
