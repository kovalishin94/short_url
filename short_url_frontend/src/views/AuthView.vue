<script setup lang="ts">
import FloatingInput from "@/components/UI/FloatingInput.vue";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();
const username = ref<string>("");
const password = ref<string>("");
const authError = ref<string>("");

async function getToken() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}api/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });
    if (response.ok) {
      clearTimeout(timeoutId);
      const data = await response.json();
      userStore.user.isAuthenticated = true;
      userStore.setTokens(data.access, data.refresh);
      router.push({ name: "urls" });
    }
    if (response.status === 401) {
      authError.value = "Неверный логин или пароль";
    }
  } catch (error) {
    username.value = "";
    password.value = "";
    userStore.removeUserData();
    authError.value = "Ошибка сервера";
  }
}
</script>

<template>
  <div class="flex h-dvh flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <div
        class="text-md bg-red-400 text-gray-800 py-2 px-6 text-center rounded-lg mb-5 transition-all duration-00"
        :class="[
          authError
            ? 'visible translate-x-0 opacity-100'
            : 'invisible -translate-x-full opacity-0',
        ]"
      >
        {{ authError }}
      </div>
      <form class="space-y-6" @submit.prevent="getToken">
        <FloatingInput id="username" type="text" v-model="username"
          >Имя пользователя</FloatingInput
        >
        <FloatingInput id="password" type="password" v-model="password"
          >Пароль</FloatingInput
        >
        <div class="flex justify-center">
          <button
            type="submit"
            class="rounded-md bg-emerald-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
          >
            Войти
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
