<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useStore } from "../composables/useStore.ts"

const $router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
const { appState, person, pictureUrl, getUser, updateUser, updatePicture } = useStore()

const fileSelector = ref()
const imageLoading = ref(true);
const busy = ref(false);

async function onSend() {
  busy.value = true;
  await updateUser();
  busy.value = false;
}

function onSelectPicture() {
  fileSelector.value.click();
}

async function onPictureSelected() {
  const localImage = fileSelector.value.files[0]
  imageLoading.value = true;
  busy.value = true;
  await updatePicture(localImage);
  imageLoading.value = false;
  busy.value = false;
}

onMounted( async () => {
  appState.isLoading = true;
  await getUser(undefined);
  if(person.value.id == "0") await $router.push({name: 'Stranger'});
  locale.value = person.value.language;

  // Preload the image
  let img = new Image();
  img.src = pictureUrl.value;
  img.onload = () => { imageLoading.value = false; };

  appState.isLoading = false;
})
</script>

<template>
  <h1>{{ person.greeting }} {{ person.name }}</h1>

  <p>{{ $t('main_challenge_1')}}
  </p>
  <p>{{ $t('main_challenge_2')}}</p>

  <div class="imageContainer centeredContainer">
    <img v-if="!imageLoading" :src="pictureUrl" alt="Your image" @click="onSelectPicture">
    <div v-else="imageBusy" class="pleaseWait">
      <div class="loader"/>
    </div>
  </div>
  <div class="textContainer">
    <textarea v-model="person.message"
              autofocus
              maxlength="1600"
              :placeholder="$t('feedback_your_message')">
    </textarea>
  </div>
  <div class="rightContainer">
    <input ref="fileSelector" type="file" @change.prevent="onPictureSelected" style="display: none"/>
    <button @click.prevent="onSend" :disabled="busy">{{ $t('feedback_send')}}</button>
  </div>
</template>

<style scoped>
@import url('../colours.css');

.pleaseWait {
  border: 1px dashed var(--accent);
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.imageContainer {
  min-width: 100%;
  min-height: 430px;
}

.imageContainer img {
  max-width: 100%;
  max-height: 430px;
  cursor: pointer;
}

.textContainer {
  width: 100%;
  display: flex;
}

textarea {
  width: 100%;
  height: 8rem;
  background-color: var(--secondary);
  color: var(--primary);
  padding: 1rem;
  border: 1px solid var(--accent);
  margin-top: 1rem;
  margin-bottom: 1rem;
  resize: vertical;
  outline: none;
  overflow: auto;
}

button {
  padding: 0.5rem 2rem;
  background-color: var(--secondary);
  color: var(--primary);
  font-weight: bold;
  border: 1px solid var(--accent);
}

button:disabled {
  background-color: var(--primary);
}
</style>
