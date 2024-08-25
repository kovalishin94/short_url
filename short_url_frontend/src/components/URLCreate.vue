<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import CopyToClipboardIcon from "./Icons/CopyToClipboardIcon.vue";

const userStore = useUserStore();
const origUrl = ref<string>("");
const shortedUrl = ref<string>("");

async function createShortUrl() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}api/urls/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userStore.user.accessToken}`,
      },
      body: JSON.stringify({
        orig_url: origUrl.value,
      }),
    });
    const data = await response.json();
    shortedUrl.value = data.shorted_url;
    origUrl.value = "";
  } catch (error) {
    console.error(error);
  }
}

function copyToClipboard() {
  navigator.clipboard.writeText(shortedUrl.value);
}
</script>
<template>
  <div
    v-if="shortedUrl"
    class="flex flex-col p-4 gap-y-3 text-center items-center"
  >
    <h1 class="text-2xl">Ваша короткая ссылка:</h1>
    <div class="flex px-5 py-2 text-3xl gap-x-4">
      {{ shortedUrl }}
      <button
        @click="copyToClipboard"
        class="hover:scale-110 transition-transform duration-300"
      >
        <CopyToClipboardIcon class="w-8 h-8" />
      </button>
    </div>
    <button
      @click="shortedUrl = ''"
      class="rounded-md bg-emerald-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
    >
      Создать новую
    </button>
  </div>
  <form
    v-else
    @submit.prevent="createShortUrl"
    class="flex flex-col p-4 gap-y-3 text-center items-center"
  >
    <label for="input" class="text-2xl">Введите вашу ссылку:</label>
    <input
      v-model="origUrl"
      id="url-input"
      type="text"
      class="py-4 px-6 border-emerald-800 outline-emerald-800 border-2 rounded-lg text-xl w-4/6"
    />
    <button
      class="rounded-md bg-emerald-600 px-12 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
    >
      Создать короткую
    </button>
  </form>
</template>
