<script setup lang="ts">
import {Ref, ref} from "vue";
import {useRouter} from "vue-router";
import {useXmasStore, XMasPerson} from "../stores/useXmasStore.ts";

const xmasStore = useXmasStore();
const router = useRouter();

const busy: Ref<boolean> = ref(false)
const newForm = ref(null)
let model: Ref<XMasPerson> = ref(new XMasPerson())

async function onBack() {
  await router.push({name: 'Landing'})
}

async function onSubmit() {
  busy.value = true;
  await xmasStore.create(model.value)
  busy.value = false;
  await onBack()
}
</script>

<template>
  <q-form ref="newForm" autofocus @submit.prevent="onSubmit">
    <div class="row nowrap">
      <q-btn flat icon="arrow_back_ios" @click="onBack"/>
      <h4>{{ model.name }}</h4>
    </div>
    <div class="row q-col-gutter-x-md q-col-gutter-y-md items-center">
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
          label="Cancel"
          color="secondary"
          tabindex="6"
          @click="onBack"
      />
    </div>
  </q-form>
</template>

<style scoped>

</style>