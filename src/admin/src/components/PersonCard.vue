<script setup lang="ts">
import { XMasFeedback, XMasPerson } from "../stores/useXmasStore.ts"
import { useBlob } from "../composables/useBlob.ts"

const { person } = defineProps<{
  person: XMasPerson;
}>();
defineEmits<{
  (e: 'onEdit', id: string): void;
}>();

const { blob } = useBlob();

function pictureSrcForYear(year: number) {
  const feedbacks = person.feedback.filter( (f: XMasFeedback) => f.year == year);
  if(feedbacks.length == 0 || ! feedbacks[0].hasPicture) return { src: '/no-image.png', label: 'No image was uploaded' }
  const blobClient = blob.containerClient?.getBlobClient(person.id)
  if(blobClient === undefined) throw Error("Failed to create blob client")
  return { src: blobClient.url, label: '' }
}

function toString(num: number): string {
  return String(num)
}
</script>

<template>
    <q-card
        class="q-gutter-x"
        style="width: 100%; margin: 10px;">
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs idSection">
          <div class="text-overline">{{ person.id }}</div>
          <div class="text-h5 q-mt-sm q-mb-xs">{{ person.name }}</div>
        </q-card-section>
        <q-separator vertical/>
        <q-card-section class="q-pt-xs configSection">
          <div class="text-overline">Configuration</div>
          <q-markup-table dense flat>
            <tbody>
              <tr>
                <td class="text-left"><b>Greeting</b></td>
                <td class="text-right">{{ person.greeting }}</td>
              </tr>
              <tr>
                <td class="text-left"><b>Language</b></td>
                <td class="text-right">{{ person.language }}</td>
              </tr>
              <tr>
                <td class="text-left"><b>Eligible for current year</b></td>
                <td class="text-right"><q-toggle v-model="person.eligibleForCurrentYear"/></td>
              </tr>
            </tbody>
          </q-markup-table>
        </q-card-section>
        <q-separator vertical/>
        <q-card-section class="q-pt-xs feedbackSection">
          <div class="text-overline">Feedback</div>
          <q-list>
            <q-expansion-item
              v-for="feedback of person.feedback"
              :key="feedback.year"
              :caption="toString(feedback.year)"
              :group="person.id"
              expand-separator
              default-opened
              style="min-width: 100%">
              <q-card>
                <q-card-section>
                  <div class="text-caption">{{ feedback.message }}</div>
                  <div>
                    <q-img :src="pictureSrcForYear(feedback.year).src">
                      <template v-slot:error>
                        <div class="absolute-full flex flex-center bg-secondary text-white">
                          {{ pictureSrcForYear(feedback.year).label }}
                        </div>
                      </template>
                    </q-img>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </q-card-section>
      </q-card-section>
      <q-card-actions>
        <q-btn flat @click="$emit('onEdit', person.id)">Edit</q-btn>
      </q-card-actions>
    </q-card>
</template>

<style scoped>
.idSection {
  width: 20%;
}
.configSection {
  width: 30%;
}
.feedbackSection {
  width: 50%;
}
</style>