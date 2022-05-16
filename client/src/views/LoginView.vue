<script setup>
import PageHeader from "../components/PageHeader.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import service from "../service/service.js";

const router = useRouter();

const email = ref(null);
const password = ref(null);
const statusRef = ref(null);

const login = async () => {
  const response = await service.jsonAPI(
    "login",
    JSON.stringify({
      email: email.value,
      password: password.value,
    })
  );
  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data));
    router.push("/");
  } else {
    statusRef.value.innerHTML = response.error;
  }
};
</script>

<template>
  <PageHeader />
  <div class="container">
    <form @submit.prevent="login">
      <label
        >Email: <input v-model="email" placeholder="email" required
      /></label>
      <label
        >Password:
        <input
          type="password"
          v-model="password"
          placeholder="password"
          required
      /></label>
      <button type="submit">Log in</button>
    </form>
    <p ref="statusRef"></p>
  </div>
</template>

<style>
@import "@/assets/style.css";

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  font-size: 24px;
}
</style>
