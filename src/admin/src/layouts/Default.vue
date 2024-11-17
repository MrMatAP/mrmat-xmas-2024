<script setup lang="ts">
import {state, useAuth} from "../composables/useAuth.ts";
const { login, logout } = useAuth();

const handleLogin = async () => {
  await login();
}

const handleLogout = async () => {
  await logout();
}
</script>

<template>
  <q-layout>
    <q-header elevated class="bg-primary">
      <q-toolbar>
        <q-toolbar-title>MrMat :: Xmas :: Admin</q-toolbar-title>
        <q-btn flat dense v-if="state.isAuthenticated" @click="handleLogout">{{ state.user.name }}</q-btn>
        <q-btn flat dense v-else @click="handleLogin">Log in</q-btn>
      </q-toolbar>
      <q-space/>
    </q-header>
    <q-page-container>
      <div id="content">
        <router-view v-if="state.isAuthenticated"></router-view>
        <p id="loginfirst" v-else>Please log in first</p>
      </div>
    </q-page-container>
  </q-layout>
</template>

<style lang="sass">
#content
  padding: 1em
#loginfirst
  vertical-align: middle
  align-content: center
</style>