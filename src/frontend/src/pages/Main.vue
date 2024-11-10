<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useStore } from "../composables/useStore.ts"

const $router = useRouter()
const { locale } = useI18n({ useScope: 'global' })
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
  locale.value = person.value.language;
  appState.isLoading = false;
})
</script>

<template>
  <h1>{{ person.greeting }} {{ person.name }}</h1>
  <p>{{ $t('main_challenge_1')}}
  </p>
  <p>{{ $t('main_challenge_2')}}</p>

  <div class="form">
    <div class="imagePlaceholder">
      <img v-show="!uploading" :src="pictureUrl" alt="Your image" @click="onSelectPicture">
    </div>
    <textarea v-model="person.message" autofocus maxlength="1000" :placeholder="$t('feedback_your_message')"></textarea>
    <div class="operations">
      <div v-show="! uploading">
        <input ref="fileSelector" type="file" @change.prevent="onPictureSelected" style="display: none"/>
        <button @click.prevent="onSend" :disabled="uploading">{{ $t('feedback_send')}}</button>
      </div>
    </div>

    <div v-show="uploading" class="overlay">
      <div class="loader"></div>
    </div>
  </div>
</template>

<style lang="scss">

</style>
