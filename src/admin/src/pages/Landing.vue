<script setup lang="ts">
import { ref, Ref, computed } from "vue";
import { useRouter } from 'vue-router';
import { useXmasStore } from "../stores/useXmasStore.ts";
import PersonCard from '../components/PersonCard.vue'

const router = useRouter();
const xmasStore = useXmasStore();

const selectedFilter: Ref<string> = ref("all")
const allPeople = computed( () => Array.from(xmasStore.people.values()))
const eligiblePeople = computed( () => allPeople.value.filter( (p) => p.eligibleForCurrentYear ) )
const people2023 = computed( () => allPeople.value.filter( (p) => p.feedback.some( (f) => f.year == 2023)))
const people2024 = computed( () => allPeople.value.filter( (p) => p.feedback.some( (f) => f.year == 2024)))

const filterOptions = [
  { label: `All (${allPeople.value.length})`, value: 'all' },
  { label: `Eligible (${eligiblePeople.value.length})`, value: 'eligible' },
  { label: `2023 (${people2023.value.length})`, value: '2023' },
  { label: `2024 (${people2024.value.length})`, value: '2024' }
]
const selection = computed(() => {
  switch(selectedFilter.value) {
    case 'all': return allPeople.value;
    case 'eligible': return eligiblePeople.value;
    case '2023': return people2023.value;
    case '2024': return people2024.value;
    default: return [];
  }
})

async function onNew() {
  await router.push({ name: 'PersonNew' })
}

async function onEdit(id: string) {
  await router.push({ name: 'PersonEdit', params: { id: id } })
}
</script>

<template>
  <div class="q-pa-md">
    <div class="row items-center">
      <div class="col-6">
        <q-option-group
            v-model="selectedFilter"
            :options="filterOptions"
            color="primary"
            inline
            dense/>
      </div>
      <div class="col-g items-end">
        <q-btn flat @click="onNew">New</q-btn>
      </div>
    </div>
  </div>
  <div class="q-pa-md">
    <div class="column q-col-gutter-lg">
      <PersonCard
          v-for="person of selection"
          :key="person.id"
          :person="person"
          @onEdit="onEdit" />
    </div>
  </div>
</template>

<style scoped>

</style>