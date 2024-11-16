<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useAppInsights } from "../composables/useAppInsights.ts";
import { useStore } from "../composables/useStore.ts"

const $router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
const { appInsights } = useAppInsights();
const { appState, person, pictureUrl, getUser, updateUser, updatePicture } = useStore()

const fileSelector = ref()
const imageLoading = ref(true);
const busy = ref(false);

async function onSendMessage() {
  busy.value = true;
  await updateUser();
  busy.value = false;
  appInsights.value.trackEvent({
    name: 'onSendMessage',
    properties: {
      person_id: person.value.id,
      person_name: person.value.name
    }
  })
}

function onSelectPicture() {
  fileSelector.value.click();
  appInsights.value.trackEvent({
    name: 'onSelectPicture',
    properties: {
      person_id: person.value.id,
      person_name: person.value.name
    }
  })
}

async function onPictureSelected() {
  const localImage = fileSelector.value.files[0]
  imageLoading.value = true;
  busy.value = true;
  await updatePicture(localImage);
  imageLoading.value = false;
  busy.value = false;
  appInsights.value.trackEvent({
    name: 'onPictureSelected',
    properties: {
      person_id: person.value.id,
      person_name: person.value.name
    }
  })
}

onMounted( async () => {
  appState.isLoading = true;
  await getUser(undefined);
  if(person.value.id == "0") await $router.push({name: 'Stranger'});
  appInsights.value.setAuthenticatedUserContext(
      person.value.id,
      person.value.name,
      true)
  appInsights.value.trackPageView({
    name: 'main',
    properties: {
      person_id: person.value.id,
      person_name: person.value.name
    }
  })
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
    <div v-else class="pleaseWait">
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
    <button @click.prevent="onSendMessage" :disabled="busy">{{ $t('feedback_send')}}</button>
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
