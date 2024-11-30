<script setup lang="ts">
import { onMounted, Ref, ref} from 'vue';
import { XMasFeedback } from "../stores/useXmasStore.ts";

const { uid, feedback } = defineProps<{
  uid: String;
  feedback: XMasFeedback;
}>();

const pictureLabel: Ref<string> = ref('No image yet')
const pictureURL: Ref<string> = ref('')

onMounted(async () => {
  if(! feedback.hasPicture) {
    pictureLabel.value = `No image`
    return;
  }
  try {
    pictureURL.value = `${import.meta.env.VITE_BLOB_URL}${import.meta.env.VITE_BLOB_CONTAINER}/${feedback.year}/${uid}?${import.meta.env.VITE_BLOB_SAS_TOKEN}`
    pictureLabel.value = ''
  } catch (e) {
    console.error(e);
  }
})
</script>

<template>
  <q-card>
    <q-card-section>
      <div class="text-caption">{{ feedback.message }}</div>
      <div>
        <q-img :src="pictureURL">
          <template v-slot:error>
            <div class="absolute-full flex flex-center bg-secondary text-white">{{ pictureLabel }}</div>
          </template>
        </q-img>
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped>

</style>