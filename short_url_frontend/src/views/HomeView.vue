<script setup lang="ts">
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
</script>

<template>
  <main>
    <h1>Hello World</h1>
    <button
      @click="userStore.removeUserData"
      class="border-2 py-2 px-6 border-gray-900 rounded-md"
    >
      Выход
    </button>
  </main>
</template>
