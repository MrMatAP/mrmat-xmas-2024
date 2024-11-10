<script setup lang="ts">
import { computed, ref, Ref, onMounted } from 'vue';
import { useStore, XMasFeedback } from "../composables/useStore.ts"

const { identity, updateFeedback, updatePicture } = useStore()

const currentFeedback = computed( () => {
  let feedback2024 = identity.value.feedback.filter( (f) => f.year == 2024)
  if(feedback2024.length == 0) return new XMasFeedback()
  return feedback2024[0]
})
const fileSelector = ref()
const uploading = ref(false);

const message: Ref<string> = ref("")
const pictureURL: Ref<string> = ref('/tap-to-update.png')

async function onSend() {
  uploading.value = true;
  await updateFeedback(message.value)
  uploading.value = false;
}

function onSelectPicture() {
  fileSelector.value.click();
}

async function onPictureSelected() {
  const localImage = fileSelector.value.files[0]
  uploading.value = true
  await updatePicture(localImage)
  pictureURL.value = `/api/pictures/${identity.value.id}`
  uploading.value = false
}

onMounted(() => {
  message.value = currentFeedback.value.message
  pictureURL.value = currentFeedback.value.hasPicture ? `/api/pictures/${identity.value.id}` : '/tap-to-update.png'
})
</script>

<template>
  <h1>{{ identity.greeting }} {{ identity.name }}</h1>
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
      <img v-show="!uploading" :src="pictureURL" alt="Your image" @click="onSelectPicture">
    </div>
    <textarea v-model="message" autofocus maxlength="1000"></textarea>
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
.imagePlaceholder {
  max-width: 80%;
  cursor: pointer;
}

.imagePlaceholder img {
  max-width: 80%;
  min-height: 400px;
}
</style>
