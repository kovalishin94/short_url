<script setup lang="ts">
import HomeIcon from "@/components/Icons/HomeIcon.vue";
</script>

<template>
  <div class="h-dvh flex justify-center items-center bg-white">
    <div class="flex flex-col items-center">
      <p class="text-5xl font-semibold text-emerald-600">404</p>
      <h1
        class="mt-4 text-3xl font-bold tracking-tight text-gray-700 sm:text-5xl"
      >
        Страница не найдена
      </h1>

      <RouterLink
        :to="{ name: 'urls' }"
        class="mt-8 rounded-md bg-emerald-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
      >
        <HomeIcon />
      </RouterLink>
    </div>
  </div>
</template>
