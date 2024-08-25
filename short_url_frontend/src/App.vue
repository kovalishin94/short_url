<script setup lang="ts">
import { RouterView } from "vue-router";
import { useUserStore } from "./stores/user";

const userStore = useUserStore();
userStore.initUser();
</script>

<template>
  <RouterView />
</template>
