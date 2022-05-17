<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
let user = JSON.parse(localStorage.getItem("user"));

const logout = () => {
  localStorage.removeItem("user");
  user = null;
  router.push("/");
};

const userMessage = computed( () => {
  return user ? `Welcome, ${user.name}!` : "";
});
</script>

<template>
  <div class="page-header">
    <h1>Voice Recognition in Japanese with Vosk</h1>
    <div class="nav-bar">
      <button @click="router.push('/')">Drill</button>
      <button @click="router.push('/admin')">Admin</button>
    </div>
    <p v-if="user">{{ userMessage }}</p>
    <button v-if="user" @click="logout">Logout</button>
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
