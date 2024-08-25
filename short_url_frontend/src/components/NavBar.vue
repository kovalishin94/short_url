<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { RouterLink, useRoute } from "vue-router";
const userStore = useUserStore();
const route = useRoute();
</script>

<template>
  <div class="flex justify-between items-center h-20 p-6">
    <div class="flex gap-x-4">
      <RouterLink
        :to="{ name: 'urls-create' }"
        class="hover:text-emerald-700 transition-colors duration-100"
        :class="{ 'text-emerald-700 font-bold': route.name === 'urls-create' }"
        >Новая ссылка</RouterLink
      >
      <RouterLink
        :to="{ name: 'urls' }"
        class="hover:text-emerald-700 transition-colors duration-100"
        :class="{ 'text-emerald-700 font-bold': route.name === 'urls' }"
        >Список ссылок</RouterLink
      >
      <RouterLink
        v-if="userStore.user.is_superuser"
        :to="{ name: 'users' }"
        class="hover:text-emerald-700 transition-colors duration-100"
        :class="{ 'text-emerald-700 font-bold': route.name === 'users' }"
        >Пользователи</RouterLink
      >
    </div>
    <div class="flex">
      <div>Добро пожаловать {{ userStore.user.username }}!</div>
      <div class="mx-4">|</div>
      <button
        @click="userStore.removeUserData"
        class="hover:text-emerald-700 transition-colors duration-100"
      >
        Выход
      </button>
    </div>
  </div>
</template>
