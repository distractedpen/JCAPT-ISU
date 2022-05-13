<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div class="page-header">
    <h1>Voice Recognition in Japanese with Vosk</h1>
    <div class="nav-bar">
      <button @click="router.push('/')">Drill</button>
      <button @click="router.push('/admin')">Admin</button>
    </div>
  </div>
</template>

<style>
.page-header {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.nav-bar {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
</style>
