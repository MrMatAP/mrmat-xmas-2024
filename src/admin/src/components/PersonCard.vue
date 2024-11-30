<script setup lang="ts">
import { onMounted } from 'vue';
import { XMasPerson } from "../stores/useXmasStore.ts"
import PersonImage from "./PersonImage.vue"

const { person } = defineProps<{
  person: XMasPerson;
}>();
defineEmits<{
  (e: 'onEdit', id: string): void;
}>();

function toString(num: number): string {
  return String(num)
}

onMounted(() => {
  new QRCode(document.getElementById(`qrcode_${person.id}`), {
    text: `https://mrmat-xmas.azurewebsites.net/${person.id}`,
    width: 256,
    height: 256,
  });
})
</script>

<template>
    <q-card
        class="q-gutter-x"
        style="width: 100%; margin: 10px;">
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs idSection">
          <div class="text-overline">{{ person.id }}</div>
          <div class="text-h5 q-mt-sm q-mb-xs">{{ person.name }}</div>
          <div :id="`qrcode_${person.id}`"></div>
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
              <PersonImage :uid="person.id" :feedback="feedback"/>
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