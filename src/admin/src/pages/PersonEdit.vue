<script setup lang="ts">
import {onMounted, Ref, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {useXmasStore, XMasPerson} from "../stores/useXmasStore.ts";

const xmasStore = useXmasStore();
const router = useRouter();
const route = useRoute();

const busy: Ref<boolean> = ref(false)
const showRemoveConfirmationDialog: Ref<boolean> = ref(false);
const editForm = ref(null)
const id: Ref<string> = ref("")
const model: Ref<XMasPerson> = ref(new XMasPerson())

async function onBack() {
  await router.push({name: 'Landing'})
}

async function onSubmit() {
  busy.value = true;
  await xmasStore.modify(model.value)
  busy.value = false;
  await onBack()
}

async function onRemove() {
  busy.value = true;
  await xmasStore.remove(id.value)
  busy.value = false;
  await onBack()
}

onMounted(async () => {
  busy.value = true;
  id.value = route.params.id as string;
  model.value = await xmasStore.get(id.value)
  busy.value = false;
})
</script>

<template>
  <q-dialog v-model="showRemoveConfirmationDialog" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm">Are you sure you want to remove this person?</span>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="primary" v-close-popup/>
        <q-btn flat label="Remove" color="negative" v-close-popup @click="onRemove"/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-form ref="editForm" autofocus @submit.prevent="onSubmit">
    <div class="row nowrap">
      <q-btn flat icon="arrow_back_ios" @click="onBack"/>
      <h4>{{ model.name }}</h4>
    </div>
    <div class="row q-col-gutter-x-md q-col-gutter-y-md">
      <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6 col-xl-6">
        <q-input
            name="id"
            label="Id"
            tabIndex="-1"
            readonly
            v-model="model.id"/>
      </div>
      <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2 col-xl-2">
        <q-toggle
            name="eligible"
            label="Eligible"
            tabIndex="2"
            v-model="model.eligibleForCurrentYear"/>
      </div>
    </div>
    <div class="row q-col-gutter-x-md q-col-gutter-y-md">
      <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8 col-xl-8">
        <q-input
            name="name"
            label="Name"
            tabIndex="1"
            autofocus
            clearable
            v-model="model.name"/>
      </div>
    </div>
    <div class="row q-col-gutter-x-md q-col-gutter-y-md items-center">
      <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
        <q-select
            name="language"
            label="Language"
            tabIndex="3"
            :options="['en', 'de']"
            v-model="model.language"/>
      </div>
      <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
        <q-input
            name="greeting"
            label="Greeting"
            clearable
            tabIndex="4"
            v-model="model.greeting"/>
      </div>
    </div>
    <q-space/>
    <div class="row q-gutter-xl content-start" style="padding-top: 30px">
      <q-btn
          label="Save"
          color="primary"
          tabIndex="5"
          @click="onSubmit"
          :loading="busy">
        <template v-slot:loading>
          <q-spinner/>
        </template>
      </q-btn>
      <q-btn
          label="Remove"
          color="negative"
          tabIndex="6"
          @click="showRemoveConfirmationDialog = true"/>
      <q-btn
          label="Cancel"
          color="secondary"
          tabindex="7"
          @click="onBack"
      />
    </div>
  </q-form>
</template>

<style scoped>

</style>